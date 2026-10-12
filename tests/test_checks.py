from dataclasses import replace

import pytest

from enclosure.checks import (
    Check,
    Check_All,
    checkHoleAndBend,
    checkHoleDiameter,
    checkShelfLength,
)
from enclosure.flat_pattern import flat_pattern
from enclosure.params import EnclosureParams


@pytest.fixture
def params():
    """Эталонный корпус: L=196, W=116, H=58.5, t=1.5, r=1.5, k=0.4."""
    return EnclosureParams(length=196, width=116, height=58.5, t=1.5, r=1.5, k=0.4)


@pytest.fixture
def shape(params):
    return flat_pattern(params)


def hole_near_bend_shape(shape, distance_to_bend):
    """Копия развёртки: один отверстие на заданном расстоянии от линии гиба x1."""
    x1, _ = shape.outline[11]
    _, y_mid = shape.circle_center[0]
    return replace(shape, circle_center=[(x1 + distance_to_bend, y_mid)])


# --- эталон: все проверки проходят ---


def test_check_all_returns_three_results(params, shape):
    results = Check_All(params, shape)
    assert len(results) == 3
    assert all(isinstance(result, Check) for result in results)


def test_reference_passes_all_checks(params, shape):
    assert all(result.passed for result in Check_All(params, shape))


def test_hole_and_bend_reference_numbers(params, shape):
    result = checkHoleAndBend(shape, params)
    assert result.actual == pytest.approx(34.95, abs=0.01)
    assert result.required == pytest.approx(4.5)
    assert result.passed


def test_hole_diameter_reference_numbers(params, shape):
    result = checkHoleDiameter(params, shape)
    assert result.actual == pytest.approx(3.4)
    assert result.required == pytest.approx(1.5)
    assert result.passed


def test_shelf_length_reference_numbers(params):
    result = checkShelfLength(params)
    assert result.actual == pytest.approx(55.5)
    assert result.required == pytest.approx(4.5)
    assert result.passed


def test_shelf_length_depends_on_angle(params):
    # при 0° ossb = 0, значит полка равна всей высоте H
    assert checkShelfLength(params, 0).actual == pytest.approx(58.5)


# --- нарушения: проверки возвращают passed=False ---


def test_hole_too_close_to_bend_fails(params, shape):
    close = hole_near_bend_shape(shape, distance_to_bend=5)
    result = checkHoleAndBend(close, params)
    assert result.actual == pytest.approx(5 - 1.7, abs=0.01)
    assert not result.passed


def test_hole_far_from_bend_passes(params, shape):
    far = hole_near_bend_shape(shape, distance_to_bend=20)
    assert checkHoleAndBend(far, params).passed


def test_nearest_hole_is_found_wherever_it_is_in_the_list(params, shape):
    """Ближайшее отверстие должно находиться и в начале, и в конце списка."""
    x1, _ = shape.outline[11]
    _, y_mid = shape.circle_center[0]
    far = (x1 + 60, y_mid)
    near = (x1 + 5, y_mid)

    near_last = replace(shape, circle_center=[far, near])
    near_first = replace(shape, circle_center=[near, far])

    assert not checkHoleAndBend(near_last, params).passed
    assert not checkHoleAndBend(near_first, params).passed
    assert checkHoleAndBend(near_last, params).actual == pytest.approx(
        checkHoleAndBend(near_first, params).actual
    )


def test_hole_diameter_smaller_than_thickness_fails():
    thick = EnclosureParams(length=196, width=116, height=58.5, t=4, r=1.5, k=0.4)
    result = checkHoleDiameter(thick, flat_pattern(thick))
    assert result.actual == pytest.approx(3.4)
    assert result.required == pytest.approx(4)
    assert not result.passed


def test_short_shelf_fails():
    short = EnclosureParams(length=196, width=116, height=6, t=1.5, r=1.5, k=0.4)
    result = checkShelfLength(short)
    assert result.actual == pytest.approx(3)
    assert result.required == pytest.approx(4.5)
    assert not result.passed


def test_result_is_immutable(params):
    result = checkShelfLength(params)
    with pytest.raises(Exception):
        result.passed = False