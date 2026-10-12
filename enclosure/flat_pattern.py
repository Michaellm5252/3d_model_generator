from dataclasses import dataclass
from enclosure.bend import bend_allowance, flat_size

@dataclass(frozen=True)
class Shape:
    outline: list[tuple[float,float]]
    bends: list[tuple[tuple[float,float], tuple[float,float]]]
    circle_center: list[ tuple[float,float]]
    circle_diameter: float

def flat_pattern(params, angle = 90):
    lf, wf = flat_size(params,angle)
    s = params.ossb(angle)
    ba = bend_allowance(params,angle)
    a = (params.height - s) + ba/2
    x1 = a
    x2 = lf - a
    y1 = a
    y2 = wf - a
    outline =[
        (x1,0),
        (x2,0),
        (x2,y1),
        (lf,y1),
        (lf,y2),
        (x2,y2),
        (x2,wf),
        (x1,wf),
        (x1,y2),
        (0,y2),
        (0,y1),
        (x1,y1)
    ]
    bends = [
        ((x1,y1),(x2,y1)),
        ((x2,y1),(x2,y2)),
        ((x2,y2),(x1,y2)),
        ((x1,y2),(x1,y1))
    ]
    circle_center = [
        (((x1+x2)/2)+60,(y1+y2)/2),
        (((x1+x2)/2)-60,(y1+y2)/2),
    ]
    circle_diameter = 3.4
    return Shape(outline,bends,circle_center, circle_diameter)