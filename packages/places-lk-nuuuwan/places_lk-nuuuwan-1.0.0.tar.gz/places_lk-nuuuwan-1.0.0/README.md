# Places in Sri Lanka (places_lk)

A utility library for returning the location (latitude and longitude) of places in Sri Lanka.

## Usage

```python
from places_lk import search_places

places = search_places('Colombo', limit=1)
print(places)

>> [{'name': 'Colombo', 'latlng': [6.93194, 79.84778]}]
```

## Install

```bash
pip install places_lk-nuuuwan
``