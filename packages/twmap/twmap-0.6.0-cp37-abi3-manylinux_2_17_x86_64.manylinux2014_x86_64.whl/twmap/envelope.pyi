from typing import Literal

from .env_points import EnvPoints

EnvelopesKind = Literal['Position', 'Color', 'Sound']


class Envelope:
    name: str
    points: EnvPoints
    def kind(self) -> EnvelopesKind:
        ...
