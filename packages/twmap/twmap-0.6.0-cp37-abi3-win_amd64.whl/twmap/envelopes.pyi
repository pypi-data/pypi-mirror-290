from typing import Iterator, Literal

from .envelope import Envelope

EnvelopesKind = Literal['Position', 'Color', 'Sound']

class Envelopes:
    def new(self, kind: EnvelopesKind) -> Envelope:
        ...
    def __len__(self) -> int:
        ...
    def __iter__(self) -> Iterator[Envelope]:
        ...
    def __next__(self) -> Envelope:
        ...
    def __getitem__(self, index: int) -> Envelope:
        ...
