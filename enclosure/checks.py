from dataclasses import dataclass
from enclosure.flat_pattern import Shape


@dataclass(frozen = True)
class  Check:
    name: str
    actual: float
    required: float
    passed: bool = False
def checkHoleAndBend(shape: Shape, params):
    list_min = []
    for center in shape.circle_center:
        cx, cy = center
        for bend in shape.bends:
            start, end = bend
            list_min.append(min(abs(cx - end[0]), abs(cy - end[1]), abs(cx - start[0]), abs(cy - start[1])))
    nearest = list_min[0]
    for min_l in list_min:
        if min_l < nearest:
            nearest = min_l
    if nearest - shape.circle_diameter / 2 >= 2*params.t + params.r:
        return Check(
            "минимальное расстояние от отверстий до линии гиба",
            nearest - shape.circle_diameter/2,
            2*params.t +params.r,
            True
        )
    else:
        return Check(
            "минимальное расстояние от отверстий до линии гиба",
            nearest - shape.circle_diameter / 2,
            2 * params.t + params.r,
            False
        )



def checkHoleDiameter(params, shape: Shape):
    if shape.circle_diameter >= params.t:
        return Check(
            "диаметр отверстия больше толщины",
            shape.circle_diameter,
            params.t,
            True
        )
    else:
        return  Check(
            "диаметр отверстия больше толщины",
            shape.circle_diameter,
            params.t,
            False
        )

def checkShelfLength(params, angle = 90):
    if params.height -params.ossb(angle) >= 3 * params.t:
        return Check(
            "длина полки",
            params.height - params.ossb(angle),
            3*params.t,
            True
        )
    else:
        return Check(
            "длина полки",
            params.height - params.ossb(angle),
            3 * params.t,
            False
        )

def Check_All(params, shape: Shape, angle = 90):
    results = []
    Checkhole = checkHoleAndBend(shape, params)
    results.append(Checkhole)
    CheckDiameter = checkHoleDiameter(params, shape)
    results.append(CheckDiameter)
    CheckShelf = checkShelfLength(params, angle)
    results.append(CheckShelf)
    return results