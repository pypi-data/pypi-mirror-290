from .layers import Layers

class Group:
    name: str
    layers: Layers
    offset_x: float
    offset_y: float
    parallax_x: float
    parallax_y: float
    clipping: bool
    clip_x: float
    clip_y: float
    clip_width: float
    clip_height: float
    def is_physics_group(self) -> bool:
        ...
