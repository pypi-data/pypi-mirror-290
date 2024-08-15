import pytest

from ICPSR.health.monitor import ComponentState

def test_valid_status():
    comp = ComponentState('Example', 'PASS', 'description', 'https://example.com', {})
    comp = ComponentState('Example', 'WARN', 'description', 'https://example.com', {})
    comp = ComponentState('Example', 'FAIL', 'description', 'https://example.com', {})

    with pytest.raises(ValueError):
        comp = ComponentState('Example', 'XXX', 'description', 'https://example.com', {})


def test_equality():
    comp1 = ComponentState('Example', 'PASS', 'description', 'https://example.com', {})
    comp2 = ComponentState('Example', 'PASS', 'description', 'https://example.com', {})
    assert comp1 == comp2

    comp1.status = 'WARN'
    assert comp1 != comp2