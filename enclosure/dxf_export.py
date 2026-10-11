import ezdxf
from ezdxf import units
from enclosure.flat_pattern import Shape

def export_dxf(shape: Shape, path):
    dxf = ezdxf.new("R2010",setup = True)
    dxf.units = units.MM
    dxf.layers.add("CUT", color = 1)
    dxf.layers.add("BEND", color = 5, linetype = "DASHED")
    msp = dxf.modelspace()
    msp.add_lwpolyline(shape.outline, close = True, dxfattribs={"layer":"CUT"})
    for start, end in shape.bends:
        msp.add_line(start, end, dxfattribs={"layer":"BEND"})
    dxf.saveas(path)