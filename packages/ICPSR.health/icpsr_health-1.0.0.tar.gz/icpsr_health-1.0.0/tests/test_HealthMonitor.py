import pytest
from datetime import datetime, timedelta
from collections import OrderedDict
import threading
from time import sleep

import ICPSR.health.monitor as health
from ICPSR.health.monitor import ComponentState, StatusObject, HealthMonitor


# === FIXTURES ===

@pytest.fixture
def mock_time_now(mocker):
    """ Fixture to freeze the `datetime.now` value.

    Creates a mock of the current datetime and patches the :py:meth:`datetime.now` method
    in the :py:mod:`ICPSR.health.monitor` module to return this mocked datetime.
    This is useful for testing the :py:attr:`HealthMonitor._last_refresh` value.
    """

    mock_time_now = datetime.now()
    mock_datetime = mocker.Mock()
    mock_datetime.now.return_value = mock_time_now
    mocker.patch.object(health, 'datetime', new=mock_datetime)
    return mock_time_now


@pytest.fixture(scope='module')
def component_fixture():
    return ComponentState('Example', status='PASS', description='', link='example.com', details={'error': None})

@pytest.fixture
def status_object_fixture(component_fixture):
    return StatusObject(component_fixture)

@pytest.fixture
def mock_status_func(mocker, component_fixture):
    return mocker.Mock(return_value=component_fixture)

@pytest.fixture
def health_monitor_fixture(mock_status_func):
    return HealthMonitor(mock_status_func, heartbeat=1, start=False)



# === TESTS ===

def test_health_monitor_defaults(mocker, mock_time_now, mock_status_func, status_object_fixture):
    """ Test the default values of the HealthMonitor constructor. """

    monitor_start_spy = mocker.spy(HealthMonitor, 'start')

    monitor = HealthMonitor(mock_status_func)

    monitor_start_spy.assert_called_once()
    assert monitor.heartbeat == 60
    assert monitor.public == ()
    assert monitor._status == status_object_fixture
    assert monitor.public_components == ()
    assert monitor._last_refresh == mock_time_now
    assert isinstance(monitor._lock, type(threading.Lock()))
    assert monitor._refresh_scheduled == True
    assert isinstance(monitor._stop_event, threading.Event)
    assert monitor._refresh_thread is not None

    monitor.release()

    # now verify defaults if the monitor is not started during initialization
    monitor = HealthMonitor(mock_status_func, start=False)

    assert monitor.heartbeat == 60
    assert monitor.public == ()
    assert monitor._status == StatusObject()
    assert monitor.public_components == ()
    assert monitor._last_refresh is None
    assert isinstance(monitor._lock, type(threading.Lock()))
    assert monitor._refresh_scheduled == False
    assert isinstance(monitor._stop_event, threading.Event)
    assert monitor._refresh_thread is None



def test_health_monitor_constructor(mock_status_func):
    """ Test the constructor of the HealthMonitor class.

    Verifies that the HealthMonitor constructor correctly initializes
    when provided with either keyword arguments or positional arguments.
    """

    test_args = OrderedDict([
        ('heartbeat', 99),
        ('public', ['foo','bar']),
        ('start', False)
    ])

    kwargs_monitor = HealthMonitor(mock_status_func, **test_args)
    assert kwargs_monitor.heartbeat == 99
    assert kwargs_monitor.public    == ['foo','bar']
    assert kwargs_monitor._last_refresh is None

    ## args no longer supported
    #
    # args_monitor   = HealthMonitor(mock_status_func, *test_args.values())
    # assert args_monitor.heartbeat == 99
    # assert args_monitor.public    == ['foo','bar']
    # assert args_monitor._last_refresh is None


def test_health_monitor_thread_management(health_monitor_fixture):
    """ Test the thread management of the HealthMonitor class.

    Verifies that the HealthMonitor correctly manages its async background thread.
    Ensures that starting the monitor initiates a new thread, the thread count remains
    consistent during refresh loops, and subsequent `start()` calls do not add additional threads.
    Finally, checks that the destructor releases the refresh thread.
    """

    threads = threading.enumerate()

    # initial monitor has not started, e.g. no extra threads
    monitor = health_monitor_fixture
    assert len(threading.enumerate()) == len(threads)

    ## monitor = HealthMonitor(status_func_fixture)

    # starting the new monitor initiates a new thread
    monitor.start()
    assert len(threading.enumerate()) == len(threads) + 1

    # thread-count should remain consistent during refresh loops
    sleep(2)
    assert len(threading.enumerate()) == len(threads) + 1

    # subsequent `start()` calls should NOT add additional threads
    monitor.start()
    assert len(threading.enumerate()) == len(threads) + 1

    # finally, calling `release()` should terminate the refresh-loop thread
    monitor.release()
    assert len(threading.enumerate()) == len(threads)


# noinspection PyPropertyAccess
def test_health_monitor_protected_attributes(health_monitor_fixture, status_object_fixture):
    """ Test the protected attributes of the HealthMonitor class.

    Verifies the read-only nature of protected attributes of the HealthMonitor class.
    """

    monitor = health_monitor_fixture
    monitor.refresh()

    # test protected attributes
    with pytest.raises(AttributeError) as ex: monitor.status = None
    assert monitor.status == status_object_fixture

    monitor._last_refresh = 'foo'
    with pytest.raises(AttributeError) as ex: monitor.last_refresh = None
    assert monitor.last_refresh == 'foo'

    with pytest.raises(AttributeError) as ex: monitor.service_state = None
    assert monitor.service_state == 'UP'

    with pytest.raises(AttributeError) as ex: monitor.http_status_code = None
    assert monitor.http_status_code == 200

    with pytest.raises(AttributeError) as ex: monitor.components = None
    assert monitor.components == status_object_fixture.component_states

    monitor.public = ['Example']
    with pytest.raises(AttributeError) as ex: monitor.public_components = None
    assert monitor.public_components == status_object_fixture.component_states


def test_health_monitor_start(mocker, mock_time_now, health_monitor_fixture):
    """ Test the `start` method of the HealthMonitor class.

    Verifies that the `start` method correctly initiates the refresh loop,
    sets the appropriate flags, and starts the refresh thread.
    """

    monitor = health_monitor_fixture
    refresh_spy = mocker.spy(monitor, 'refresh')
    refresh_loop_spy = mocker.spy(monitor, '_refresh_loop')

    assert monitor._refresh_scheduled == False
    assert monitor._refresh_thread is None
    assert isinstance(monitor._stop_event, threading.Event)
    assert monitor._last_refresh is None
    refresh_loop_spy.assert_not_called()
    refresh_spy.assert_not_called()


    monitor.start()

    refresh_loop_spy.assert_called_once()
    refresh_spy.assert_called_once()
    assert monitor._refresh_scheduled
    assert not monitor._stop_event.is_set()
    assert monitor._refresh_thread is not None
    assert monitor._refresh_thread.is_alive()
    assert monitor._last_refresh == mock_time_now

    monitor.release()


def test_health_monitor_refresh(mock_time_now, mock_status_func, health_monitor_fixture, status_object_fixture):
    """ Test the `refresh` method of the HealthMonitor class.

    Verifies that the `refresh` method correctly updates the
    monitor's status and last refresh time.
    """

    monitor = health_monitor_fixture
    assert monitor.last_refresh is None
    assert monitor._status == StatusObject()

    monitor.refresh()
    mock_status_func.assert_called_once()
    assert monitor._status == status_object_fixture
    assert monitor._last_refresh == mock_time_now


def test_health_monitor_refresh_loop(mocker, health_monitor_fixture):
    """ Test the refresh loop functionality of the HealthMonitor.

    Verifies that the HealthMonitor's refresh loop is correctly
    initiated, runs at the specified heartbeat interval, and stops as expected.
    """

    monitor = health_monitor_fixture
    monitor.heartbeat = wait = 2

    refresh_spy = mocker.spy(monitor, 'refresh')
    refresh_spy.assert_not_called()

    refresh_spy.assert_not_called()

    monitor.start()
    assert monitor._refresh_scheduled
    refresh_spy.assert_called_once()

    sleep(1)
    refresh_spy.assert_called_once()

    for i in range(3):
        assert refresh_spy.call_count == 1 + i
        sleep(wait)

    refresh_calls = refresh_spy.call_count
    monitor.stop()
    sleep(wait+1)

    assert refresh_spy.call_count == refresh_calls
    assert monitor._refresh_scheduled == False

    monitor.release()


def test_health_monitor_stop(mocker, health_monitor_fixture):
    """ Test the `stop` functionality of the HealthMonitor.

    Verifies that the HealthMonitor's `stop` method correctly halts
    the refresh loop and sets the stop event.
    """

    monitor = health_monitor_fixture

    assert not monitor._stop_event.is_set()
    assert monitor._last_refresh is None

    thread_spy = mocker.spy(monitor, '_refresh_thread')
    refresh_loop_spy = mocker.spy(monitor, '_refresh_loop')
    refresh_spy = mocker.spy(monitor, 'refresh')

    refresh_spy.assert_not_called()

    monitor.start()

    refresh_spy.assert_called()
    refresh_loop_spy.assert_called_once()

    refresh_time = monitor._last_refresh
    refresh_spy.reset_mock()

    monitor.stop()

    assert monitor._stop_event.is_set()
    refresh_spy.assert_not_called()

    sleep(2)

    refresh_spy.assert_not_called()
    assert monitor._last_refresh == refresh_time

    monitor.release()


def test_health_monitor_is_stale(mock_status_func, mock_time_now):
    """ This function tests the 'is_stale' method of the HealthMonitor class. """

    monitor = HealthMonitor(mock_status_func, heartbeat=60, start=False)

    monitor._last_refresh = mock_time_now - timedelta(seconds=59)
    assert not monitor.is_stale()

    monitor._last_refresh = mock_time_now - timedelta(seconds=60)
    assert not monitor.is_stale()

    monitor._last_refresh = mock_time_now - timedelta(seconds=61)
    assert monitor.is_stale()


def test_health_monitor_properties(mock_time_now, health_monitor_fixture, component_fixture):
    """ Verifies that the properties of the HealthMonitor instance return the expected internal values. """

    public_component = ComponentState('Public', status='FAIL', description='', link='other.net', details={})

    status_obj = StatusObject(public_component, component_fixture)

    monitor = health_monitor_fixture
    monitor.status_functions = (lambda: public_component, lambda: component_fixture)
    monitor.public = ['Public']

    monitor.refresh()

    # property getters
    assert monitor.status            == status_obj
    assert monitor.service_state     == status_obj.state
    assert monitor.http_status_code  == status_obj.code
    assert monitor.components        == status_obj.component_states
    assert monitor.public_components == (public_component,)
    assert monitor.last_refresh      == mock_time_now

    # property aliases
    assert monitor.state == monitor.service_state
    assert monitor.code  == monitor.http_status_code