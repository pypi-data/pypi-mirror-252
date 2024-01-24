from utils import Log

from places_lk.core.PLACE_INFO_LIST import PLACE_INFO_LIST

log = Log('search_places')


def search_places(search_key: str, limit: int = None):
    place_info_list = []
    search_key_lower = search_key.lower()
    for place_info in PLACE_INFO_LIST:
        if search_key_lower in place_info.name.lower():
            place_info_list.append(place_info)

            if limit and len(place_info_list) >= limit:
                break
    log.info(f'Found {len(place_info_list)} places for "{search_key}".')
    return place_info_list


def search_places_smart(func_search: callable):
    matches = [
        place_info
        for place_info in PLACE_INFO_LIST
        if func_search(place_info)
    ]
    log.info(f'Found {len(matches)} places.')
    return matches
