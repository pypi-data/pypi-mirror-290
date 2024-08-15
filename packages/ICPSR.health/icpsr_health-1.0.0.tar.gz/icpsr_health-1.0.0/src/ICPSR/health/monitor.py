import logging
import threading
from datetime import datetime, timedelta
from typing import Literal, Callable, Sequence, cast, get_args


# === TELEMETRY ===

# trace.set_tracer_provider(telemetry_provider)
# tracer = trace.get_tracer(__name__)


# === HEALTH CLASSES ===

class ComponentState:
    """ A simple object representing the status of a single component.

    Arguments:
        name: The name of the component.
        status: The status of the component ('UP' or 'DOWN').
        description: A brief description of the component.
        link: A link to more information about the component.
        details: Additional details about the component.
    """

    T = Literal['PASS', 'WARN', 'FAIL']  # acceptable service states

    def __init__(self, name:str, /, status:T, description:str, link:str, details:dict):
        """ A simple object representing the status of a single component.

        Parameters:
            name: The name of the component.
            status: The status of the component ('UP' or 'DOWN').
            description: A brief description of the component.
            link: A link to more information about the component.
            details: Additional details about the component.
        """

        if status not in get_args(self.T):
            raise ValueError(f'invalid status: {status}. Must be one of {get_args(self.T)}.')

        self.name:str = name
        self.status:ComponentState.T = status
        self.description:str = description
        self.link:str = link
        self.details:dict = details

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



class StatusObject:
    """
    Class representing the overall health status of the service.

    Attributes:
        component_states: A list containing the :py:class:`ComponentState` for various components.

    Read-only Properties:
        - ``state`` – The overall state of the service.
        - ``code`` – The HTTP status code corresponding to the service state.
    """

    T = Literal['UP', 'DOWN']  # acceptable service states

    def __init__(self, *components:ComponentState):
        """
        Class representing the overall health status of the service.

        Parameters:
            components: A list containing the :py:class:`ComponentState` for various components.
        """

        # noinspection PyTypeChecker
        self.component_states:tuple[ComponentState] = components


    def __repr__(self):
        return str({ 'state': self.state, 'code': self.code, 'components': [comp.name for comp in self.component_states] })

    def __eq__(self, other):
        if not isinstance(other, StatusObject):
            raise TypeError(f"can't compare StatusObject with {type(other).__name__}")

        # if all components of each objet have the same internals, then the two objects are equal
        return { comp.name: comp for comp in self.component_states } == { comp.name: comp for comp in other.component_states }


    # noinspection PyTypeChecker
    @property
    def component_states(self) -> tuple[ComponentState]:
        """List containing the :py:class:`ComponentState` of various dependencies."""
        return self._components


    @component_states.setter
    def component_states(self, components:Sequence[ComponentState]):
        self._components = tuple(components)

        try:
            for comp in components:
                if not isinstance(comp, ComponentState):
                    raise TypeError(f"argument '{comp}' is not a valid component!")

            component_states = set(comp.status for comp in components)
            if not components:
                self._state = 'UP'  # default state when there are no components
                self._code = 200  # OK
            elif 'FAIL' in component_states:
                # if there are no components or ANY of the components' status is "FAIL"
                self._state = 'DOWN'
                self._code = 503  # SERVICE UNAVAILABLE
            elif component_states == {'PASS'}:
                self._state = 'UP'
                self._code = 200  # OK
            elif component_states == {'PASS', 'WARN'}:
                self._state = 'UP'
                self._code = 207  # MULTI-STATUS
            elif component_states == {'WARN'}:
                self._state = 'WARN'
                self._code = 218  # THIS IS FINE (a catch-all error condition when the service appears to still be functional)
            else:
                invalid = component_states - {'WARN', 'PASS', 'FAIL'}
                raise ValueError(f"invalid component status {invalid} -- must be one of {get_args(ComponentState.T)}")

        except Exception as ex:
            self._state = 'DOWN'
            self._code = 500  # INTERNAL SERVER ERROR
            logging.exception(ex)


    @property
    def state(self) -> T:
        """The overall state of the service."""
        return cast(self.T, self._state)


    @property
    def code(self) -> int:
        """The HTTP status code corresponding to the service state."""
        return self._code



class HealthMonitor:
    """
    A class for monitoring the health of a service.

    The HealthMonitor object refreshes a healthcheck status at a specified interval, and provides methods for checking
    the status and refreshing the cache.

    Methods:
        start(): Starts the periodic refresh of the cache.
        stop(): Halts the periodic refresh of the cache.
        refresh(): Immediately refreshes the cache by updating the _status and _public_components attributes.
        is_stale(): Checks if the cache is stale by comparing the current time with the last refresh timestamp.

    Attributes:
        status_functions: Functions used to check the status of dependencies.
        heartbeat: The rate (in seconds) at which to refresh the cached healthcheck.
        public: A list of "public" component names.
        _lock: A lock for thread-safe access to the cache.
        _refresh_scheduled: A flag indicating whether the cache refresh is scheduled.
        _stop_event: An event for stopping the cache refresh thread.

    Read-only Properties:
        - ``status`` – The current healthcheck status object.
        - ``service_state`` – The current overall state of the service.
        - ``http_status_code`` – The current HTTP status code corresponding to the service state.
        - ``components`` – The status details of individual components.
        - ``public_components`` – The status details of all "public" components.
        - ``last_refresh`` – The timestamp of the last time the cache was refreshed.
    """


    def __init__(self, *status_functions:Callable[..., ComponentState], heartbeat:int = 60, public:list[str] = tuple(), start:bool = True):
        """
        Initializes a new instance of the HealthMonitor class.

        Parameters:
            *status_functions: Functions used to check the status of dependencies.
                Each status_function should return a :py:class:`ComponentState`.
                Requires at least one value.
            heartbeat: The rate (in seconds) at which to refresh the cached healthcheck.
                Default is 60 seconds.
            public: A list of "public" components (i.e. safe for public inpsection).
                The details of these components will appear in the 'readiness' health check. Default is an empty list.
            start: Immediately begin the refresh-loop after creation.
                Defaults to True.
        """

        ## TODO: not sure if we want should allow a monitor without a status function...
        #
        # if not status_functions:
        #     raise ValueError('at least one status-function must be provided.')

        # noinspection PyTypeChecker
        self.status_functions:tuple[Callable[..., ComponentState]] = status_functions  # these functions are called to obtain the overall Service Status
        self.heartbeat:int = heartbeat  # rate (in seconds) at which to refresh the cached healthcheck
        self.public:list[str] = public  # list of "public" component names (the details of these components will appear in the 'readiness' health check)
        self._status:StatusObject = StatusObject()  # healthcheck status object
        self._last_refresh:datetime = cast(datetime, None)  # timestamp of the last time the cache was refreshed

        self._lock:threading.Lock = threading.Lock()
        self._refresh_scheduled:bool = False
        self._stop_event:threading.Event = threading.Event()
        self._refresh_thread:threading.Thread = cast(threading.Thread, None)

        if start:
            self.start()


    def __del__(self): self.release()

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_value, traceback): self.release()


    def release(self):
        """
        Halts the periodic refresh of the cached healthcheck and releases the refresh thread.
        """
        self.stop()
        if self._refresh_thread: self._refresh_thread.join()
        return self


    def start(self):
        """
        Starts the periodic refresh of the cached healthcheck.

        This method starts the periodic refresh of the cached healthcheck by calling the `refresh` method and setting the `_refresh_scheduled` flag to `True`. It also clears the `_stop_event` and starts a new thread to execute the `_refresh_loop` method.
        """

        if not self._refresh_scheduled:
            self.refresh()
            self._refresh_scheduled = True
            self._stop_event.clear()
            self._refresh_thread = threading.Thread(name='HealthMonitor._refresh_thread', target=self._refresh_loop)
            self._refresh_thread.start()

        return self


    def stop(self):
        """
        Halts the periodic refresh of the cached healthcheck.

        This method halts the periodic refresh of the cached healthcheck by settings the _stop_event attribute.
        """

        self._stop_event.set()
        return self


    def _refresh_loop(self):
        """
        This method is responsible for refreshing the cached healthcheck status at a specified interval.

        Notes:
            This method is called by the `start` method and runs in a separate thread.
        """

        while not self._stop_event.wait(timeout=self.heartbeat): # skip loop if the _stop_event attr is set, otherwise waits for the specified time and then enters the loop
            self.refresh()

        self._refresh_scheduled = False  # once we pass the loop, refresh() will no longer be triggered, so we set _refresh_scheduled to False


    def refresh(self):
        """
        Refreshes the cached healthcheck status.

        This method refreshes the cached healthcheck status by calling the `get_aggregate_status` function and updating the `_status`, `_public_components`, and `_last_refresh` attributes.
        """

        with self._lock:
            self._status.component_states = [component_status() for component_status in self.status_functions]
            self._last_refresh = datetime.now()


    def is_stale(self) -> bool:
        """
        Checks if the cache is stale by comparing the current time with the last refresh timestamp.

        Returns:
            bool: Returns True if the cache is stale, False otherwise.
        """
        return self._last_refresh < datetime.now() - timedelta(seconds=self.heartbeat)


    @property
    def status(self) -> StatusObject:
        """The current healthcheck status object."""
        return self._status


    @property
    def service_state(self) -> StatusObject.T:
        """The current overall state of the service."""
        return self._status.state
    state = service_state # alias


    @property
    def http_status_code(self) -> int:
        """The current HTTP status code corresponding to the service state."""
        return self._status.code
    code = http_status_code # alias


    # noinspection PyTypeChecker
    @property
    def components(self) -> tuple[ComponentState]:
        """The status details of all monitored components."""
        return tuple(self._status.component_states)


    # noinspection PyTypeChecker
    @property
    def public_components(self) -> tuple[ComponentState]:
        """The status details of all "public" components."""
        return tuple(comp for comp in self._status.component_states if comp.name in self.public)


    @property
    def last_refresh(self) -> datetime:
        """The timestamp of the last time the cache was refreshed."""
        return self._last_refresh


