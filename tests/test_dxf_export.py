import ezdxf
import pytest
from ezdxf import units

from enclosure.dxf_export import export_dxf
from enclosure.flat_pattern import flat_pattern
from enclosure.params import EnclosureParams


@pytest.fixture
def params():
    """Эталонный корпус: L=196, W=116, H=58.5, t=1.5, r=1.5, k=0.4."""
    return EnclosureParams(length=196, width=116, height=58.5, t=1.5, r=1.5, k=0.4)


@pytest.fixture
def shape(params):
    return flat_pattern(params)


@pytest.fixture
def doc(shape, tmp_path):
    path = tmp_path / "out.dxf"
    export_dxf(shape, str(path))
    return ezdxf.readfile(str(path))


def test_file_is_created(shape, tmp_path):
    path = tmp_path / "out.dxf"
    export_dxf(shape, str(path))
    assert path.exists()
    assert path.stat().st_size > 0


def test_units_are_millimeters(doc):
    assert doc.units == units.MM


def test_layers_exist(doc):
    names = {layer.dxf.name for layer in doc.layers}
    assert "CUT" in names
    assert "BEND" in names


def test_bend_layer_is_dashed(doc):
    assert doc.layers.get("BEND").dxf.linetype == "DASHED"


def test_outline_is_one_closed_polyline_on_cut(doc):
    polylines = doc.modelspace().query('LWPOLYLINE[layer=="CUT"]')
    assert len(polylines) == 1
    polyline = polylines[0]
    assert polyline.closed
    assert len(polyline.get_points("xy")) == 12


def test_outline_points_match_shape(doc, shape):
    polyline = doc.modelspace().query('LWPOLYLINE[layer=="CUT"]')[0]
    for written, expected in zip(polyline.get_points("xy"), shape.outline):
        assert written == pytest.approx(expected)


def test_four_bend_lines_on_bend_layer(doc):
    assert len(doc.modelspace().query('LINE[layer=="BEND"]')) == 4


def test_bend_lines_match_shape(doc, shape):
    lines = doc.modelspace().query('LINE[layer=="BEND"]')
    written = sorted(
        ((line.dxf.start.x, line.dxf.start.y), (line.dxf.end.x, line.dxf.end.y))
        for line in lines
    )
    expected = sorted(shape.bends)
    for got, want in zip(written, expected):
        assert got[0] == pytest.approx(want[0])
        assert got[1] == pytest.approx(want[1])


def test_holes_are_circles_on_cut(doc, shape):
    circles = doc.modelspace().query('CIRCLE[layer=="CUT"]')
    assert len(circles) == len(shape.circle_center)
    for circle in circles:
        assert circle.dxf.radius == pytest.approx(shape.circle_diameter / 2)


def test_hole_centers_match_shape(doc, shape):
    circles = doc.modelspace().query('CIRCLE[layer=="CUT"]')
    written = sorted((c.dxf.center.x, c.dxf.center.y) for c in circles)
    expected = sorted(shape.circle_center)
    for got, want in zip(written, expected):
        assert got == pytest.approx(want)


def test_nothing_on_other_layers(doc):
    layers = {entity.dxf.layer for entity in doc.modelspace()}
    assert layers <= {"CUT", "BEND"}