from typing import Annotated, Optional, Tuple

class Quad:
    position: Tuple[float, float]
    corners: list
    colors: Annotated[list[int], 4]
    texture_coords: Annotated[list[Tuple[float, float]], 4]
    position_env: Optional[int]
    position_env_offset: int
    color_env: Optional[int]
    color_env_offset: int
