import pytest
from enclosure.params import EnclosureParams
from enclosure.bend import bend_allowance, bend_deduction, flat_size


@pytest.fixture
def p():
    return EnclosureParams(196, 116, 58.5, 1.5, 1.5, 0.4)


def test_bend_allowance_90(p):
    assert bend_allowance(p) == pytest.approx(3.2987, abs=0.001)


def test_bend_allowance_default_is_90(p):
    assert bend_allowance(p) == pytest.approx(bend_allowance(p, 90))


def test_bend_allowance_zero_angle(p):
    assert bend_allowance(p, 0) == pytest.approx(0.0)


def test_bend_allowance_different_r_and_t():
    # r и t разные: ловит перепутанные поля
    p2 = EnclosureParams(196, 116, 58.5, 1.5, 2.0, 0.4)
    assert bend_allowance(p2) == pytest.approx(4.0841, abs=0.001)


def test_bend_deduction_90(p):
    assert bend_deduction(p) == pytest.approx(2.7013, abs=0.001)


def test_flat_size_90(p):
    length, width = flat_size(p)
    assert length == pytest.approx(307.60, abs=0.01)
    assert width == pytest.approx(227.60, abs=0.01)


def test_flat_size_default_is_90(p):
    assert flat_size(p) == pytest.approx(flat_size(p, 90))


def test_flat_size_zero_angle(p):
    # без гибов развёртка равна L + 2H и W + 2H
    length, width = flat_size(p, 0)
    assert length == pytest.approx(313.0, abs=0.01)
    assert width == pytest.approx(233.0, abs=0.01)