import math

import pytest

from enclosure.bend import flat_size
from enclosure.flat_pattern import flat_pattern
from enclosure.params import EnclosureParams


@pytest.fixture
def params():
    """Эталонный корпус: L=196, W=116, H=58.5, t=1.5, r=1.5, k=0.4."""
    return EnclosureParams(length=196, width=116, height=58.5, t=1.5, r=1.5, k=0.4)


def test_two_holes(params):
    assert len(flat_pattern(params).circle_center) == 2


def test_hole_diameter(params):
    assert flat_pattern(params).circle_diameter == pytest.approx(3.4)


def test_hole_pitch_is_120(params):
    first, second = flat_pattern(params).circle_center
    assert math.dist(first, second) == pytest.approx(120)


def test_holes_on_axis_of_enclosure(params):
    shape = flat_pattern(params)
    length_flat, width_flat = flat_size(params)
    for x, y in shape.circle_center:
        assert y == pytest.approx(width_flat / 2)
    xs = [x for x, _ in shape.circle_center]
    assert sum(xs) / 2 == pytest.approx(length_flat / 2)


def test_holes_are_inside_the_bottom(params):
    shape = flat_pattern(params)
    x1, y1 = shape.outline[11]
    x2, y2 = shape.outline[5]
    radius = shape.circle_diameter / 2
    for x, y in shape.circle_center:
        assert x - radius > x1
        assert x + radius < x2
        assert y - radius > y1
        assert y + radius < y2


def test_holes_are_symmetric(params):
    shape = flat_pattern(params)
    length_flat, _ = flat_size(params)
    left, right = sorted(x for x, _ in shape.circle_center)
    assert left + right == pytest.approx(length_flat)