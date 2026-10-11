import math

import pytest

from enclosure.bend import flat_size
from enclosure.flat_pattern import flat_pattern
from enclosure.params import EnclosureParams


@pytest.fixture
def params():
    """Эталонный корпус: L=196, W=116, H=58.5, t=1.5, r=1.5, k=0.4."""
    return EnclosureParams(length=196, width=116, height=58.5, t=1.5, r=1.5, k=0.4)


def bounding_box(points):
    xs = [x for x, _ in points]
    ys = [y for _, y in points]
    return max(xs) - min(xs), max(ys) - min(ys)


def test_reference_size_90(params):
    width, height = bounding_box(flat_pattern(params).outline)
    assert width == pytest.approx(307.60, abs=0.01)
    assert height == pytest.approx(227.60, abs=0.01)


def test_reference_size_0(params):
    width, height = bounding_box(flat_pattern(params, 0).outline)
    assert width == pytest.approx(313, abs=0.01)
    assert height == pytest.approx(233, abs=0.01)


@pytest.mark.parametrize("angle", [0, 45, 90])
def test_bounding_box_matches_flat_size(params, angle):
    width, height = bounding_box(flat_pattern(params, angle).outline)
    expected_width, expected_height = flat_size(params, angle)
    assert width == pytest.approx(expected_width)
    assert height == pytest.approx(expected_height)


def test_outline_starts_at_origin_corner(params):
    outline = flat_pattern(params).outline
    xs = [x for x, _ in outline]
    ys = [y for _, y in outline]
    assert min(xs) == pytest.approx(0)
    assert min(ys) == pytest.approx(0)


def test_counts(params):
    shape = flat_pattern(params)
    assert len(shape.outline) == 12
    assert len(shape.bends) == 4


def test_reference_points(params):
    outline = flat_pattern(params).outline
    assert outline[0] == pytest.approx((57.15, 0), abs=0.01)
    assert outline[3] == pytest.approx((307.60, 57.15), abs=0.01)
    assert outline[5] == pytest.approx((250.45, 170.45), abs=0.01)


def test_bend_line_lengths(params):
    lengths = sorted(
        math.dist(start, end) for start, end in flat_pattern(params).bends
    )
    assert lengths[0] == pytest.approx(113.30, abs=0.01)
    assert lengths[1] == pytest.approx(113.30, abs=0.01)
    assert lengths[2] == pytest.approx(193.30, abs=0.01)
    assert lengths[3] == pytest.approx(193.30, abs=0.01)


def test_bend_lines_end_at_inner_corners_of_outline(params):
    shape = flat_pattern(params)
    for start, end in shape.bends:
        for point in (start, end):
            assert any(
                math.dist(point, vertex) < 1e-9 for vertex in shape.outline
            ), f"{point} не совпадает ни с одной вершиной контура"