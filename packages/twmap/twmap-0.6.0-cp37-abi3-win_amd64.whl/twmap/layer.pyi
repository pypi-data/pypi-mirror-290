from typing import Optional, Tuple
import numpy

from .quads import Quads

class Layer:
    tiles: numpy.ndarray
    image: Optional[int]
    quads: Quads
    color: Tuple[int, int, int, int]
    name: str
    def width(self) -> int:
        ...
    def height(self) -> int:
        ...
    def kind(self) -> str:
        ...
    def to_mesh(self) -> tuple:
        ...
