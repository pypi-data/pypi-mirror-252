from dataclasses import dataclass
from functools import cached_property


@dataclass
class Alt:
    alt_m: float

    PRECISION = 0

    def __hash__(self) -> int:
        return hash(self.alt_m)

    def __str__(self) -> str:
        return f"{self.alt_m:.0f}m"

    @cached_property
    def alt_m_normalized(self) -> float:
        return round(self.alt_m, Alt.PRECISION)

    @staticmethod
    def from_str(s: str) -> 'Alt':
        return Alt(alt_m=float(s))
