import pytest
from typing import get_args

from ICPSR.health.monitor import ComponentState, StatusObject


# === HELPERS ===

COMPONENT_STATUSES = get_args(ComponentState.T)
""" Tuple of all valid statuses for a :py:class:`ComponentState` object. """

@pytest.fixture
def generate_component(mocker):
    def _generate_component(status, name='comp', description='', link='', details=None):
        """ Generates a :py:class:`ComponentState` object with the specified status, name, description, link, and details. """

        comp = ComponentState(name, 'PASS', description, link, details)

        if status not in ('PASS', 'WARN', 'FAIL'):
            mocker.patch.object(comp, 'status', status)  # fake an unacceptable status value
        else:
            comp.status = status

        return comp

    return _generate_component


# === TESTS ===

def test_status_object_no_components():
    """ Tests the behavior of the :py:class:`StatusObject` constructor when no components are provided. """

    actual = StatusObject()
    assert actual.state == 'UP'
    assert actual.code == 200  #
    assert actual.component_states == tuple()


# noinspection PyPropertyAccess
def test_status_object_read_only_attrs(generate_component):
    """ Verifies the protection of read-only attributes of the :py:class:`StatusObject`. """

    comp1 = generate_component('PASS')
    comp2 = generate_component('FAIL')

    actual = StatusObject(comp1, comp2)
    assert actual.component_states == (comp1, comp2)

    actual.component_states = tuple()
    assert actual.component_states == tuple()

    with pytest.raises(AttributeError): actual.state = 'XXX'
    with pytest.raises(AttributeError): actual.code = 000


@pytest.mark.parametrize("status1", (*COMPONENT_STATUSES, 'XXX'))
@pytest.mark.parametrize("status2", COMPONENT_STATUSES)
def test_status_object_states(status1:str, status2:str, generate_component):
    """ Tests the behavior of the :py:class:`StatusObject` for various combinations of component statuses. """

    comp1 = generate_component(status1)
    comp2 = generate_component(status2)

    actual = StatusObject(comp1, comp2)
    assert actual.component_states == (comp1, comp2)

    comps = { status1, status2 }
    if   comps == {'PASS','PASS'}:
        assert actual.state == 'UP'
        assert actual.code == 200  # OK

    elif comps == {'PASS','WARN'}:
        assert actual.state == 'UP'
        assert actual.code == 207  # MULTI-STATUS

    elif comps == {'PASS','FAIL'}:
        assert actual.state == 'DOWN'
        assert actual.code == 503  # SERVICE UNAVAILABLE

    elif comps == {'PASS','XXX'}:
        assert actual.state == 'DOWN'
        assert actual.code == 500  # INTERNAL SERVER ERROR

    elif comps == {'WARN','WARN'}:
        assert actual.state == 'WARN'
        assert actual.code == 218  # THIS IS FINE

    elif comps == {'WARN','FAIL'}:
        assert actual.state == 'DOWN'
        assert actual.code == 503  # SERVICE UNAVAILABLE

    elif comps == {'WARN','XXX'}:
        assert actual.state == 'DOWN'
        assert actual.code == 500  # INTERNAL SERVER ERROR

    elif comps == {'FAIL','FAIL'}:
        assert actual.state == 'DOWN'
        assert actual.code == 503  # SERVICE UNAVAILABLE

    elif comps == {'FAIL','XXX'}:
        assert actual.state == 'DOWN'
        assert actual.code == 503  # SERVICE UNAVAILABLE'

    else:
        raise AssertionError(f"missing test for combination {comps}!")


# noinspection PyTypeChecker
@pytest.mark.xfail(reason='currently logging exception rather than raising')
def test_invalid_components(generate_component):
    """ Tests that the :py:class:`StatusObject` raises appropriate exceptions when:

        - A component is not an instance of ComponentState.
        - A component has an invalid status value.
        - A component lacks the 'status' attribute.
    """

    comp1 = generate_component('PASS')
    comp2 = 'not a ComponentState'

    # invalid component type
    with pytest.raises(TypeError): StatusObject(comp1, comp2)

    # invalid status value
    comp2 = generate_component('XXX')
    with pytest.raises(ValueError): StatusObject(comp1, comp2)

    # no `status` attr
    del comp2.status
    with pytest.raises(AttributeError): StatusObject(comp1, comp2)