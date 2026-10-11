import math
from dataclasses import dataclass


class ParamsError(ValueError):
    """Неверные параметры корпуса."""


@dataclass(frozen=True)
class EnclosureParams:
    length: float
    width: float
    height: float
    t: float
    r: float
    k: float

    def __post_init__(self):
        for name in ("length", "width", "height", "t"):
            value = getattr(self, name)
            if value <= 0:
                raise ParamsError(f"{name} должно быть больше 0, получено {value}")
        if self.r < 0:
            raise ParamsError(f"r не может быть отрицательным, получено {self.r}")
        if not 0 < self.k <= 0.5:
            raise ParamsError(f"k должен быть в пределах (0; 0,5], получено {self.k}")
        if self.height <= self.ossb():
            raise ParamsError(
                f"height ({self.height}) должна быть больше r + t ({self.ossb()})"
            )
        for name in ("length", "width"):
            if getattr(self, name) <= 2 * self.ossb():
                raise ParamsError(
                    f"{name} должна быть больше 2·(r + t) = {2 * self.ossb()}"
                )

    def ossb(self, angle=90) -> float:
        return (self.r + self.t) * math.tan(math.radians(angle)/2)

