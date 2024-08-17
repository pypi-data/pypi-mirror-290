from typing import Literal

class EnvPoint:
    time: int
    curve: Literal['Step', 'Linear', 'Slow', 'Fast', 'Smooth', 'Bezier']

    # pos
    x: float
    y: float

    # color
    r: float
    g: float
    b: float
    a: float

    # different shape for color and pos points
    content: tuple
