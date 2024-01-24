import json
from dataclasses import dataclass
from functools import cached_property


@dataclass
class LatLng:
    lat: float
    lng: float

    PRECISION = 6

    def __hash__(self) -> int:
        return hash((self.lat, self.lng))

    def __str__(self) -> str:
        return f"({self.lat:.06f}°N {self.lng:.06f}°E"

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LatLng):
            return False
        return (self.lat == o.lat) and (self.lng == o.lng)

    @cached_property
    def lat_normalized(self) -> float:
        return round(self.lat, LatLng.PRECISION)

    @cached_property
    def lng_normalized(self) -> float:
        return round(self.lng, LatLng.PRECISION)

    @cached_property
    def tuple_normalized(self) -> tuple[float, float]:
        return (self.lat_normalized, self.lng_normalized)

    @staticmethod
    def from_str(s: str) -> 'LatLng':
        lat, lng = json.loads(s)
        return LatLng(
            lat=float(lat),
            lng=float(lng),
        )
