import json
import os
from pathlib import Path
from typing import Optional, Tuple
import requests
from loguru import logger


CACHE_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "cache" / "geocode_cache.json"


def _load_cache() -> dict:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def geocode_place(name: str, country: Optional[str] = None) -> Optional[Tuple[float, float]]:
    """Return (lat, lng) for a place, using cache -> Google -> OSM.

    - Does NOT concatenate country into the address string; instead passes
      country as a filter/bias to provider-specific params to avoid queries
      like "<name> KR KR".
    """
    key = f"{name}|{country or ''}"
    cache = _load_cache()
    if key in cache:
        lat, lng = cache[key]
        return float(lat), float(lng)

    query = name.strip()

    # Try Google Geocoding API
    gkey = os.getenv("GOOGLE_MAPS_API_KEY")
    if gkey:
        try:
            params = {"address": query, "key": gkey}
            if country:
                params["components"] = f"country:{country}"
                params["region"] = country
            r = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params, timeout=15)
            if r.ok:
                data = r.json()
                if data.get("results"):
                    loc = data["results"][0]["geometry"]["location"]
                    lat, lng = float(loc["lat"]), float(loc["lng"])
                    cache[key] = [lat, lng]
                    _save_cache(cache)
                    return lat, lng
                else:
                    logger.warning("Google Geocoding returned no results for '{}' (country={})", query, country)
            else:
                logger.warning("Google Geocoding HTTP {code} for '{}'", r.status_code, query)
        except Exception:
            logger.warning("Google Geocoding error for '{}' — falling back to OSM", query)
    else:
        logger.info("GOOGLE_MAPS_API_KEY not set. Using OSM Nominatim for '{}'", query)

    # Fallback to OSM Nominatim (be polite: include email if provided)
    headers = {"User-Agent": "agentic-market-entry/0.1"}
    email = os.getenv("OSM_NOMINATIM_EMAIL")
    try:
        params = {"q": query, "format": "json", "limit": 1, **({"email": email} if email else {})}
        if country:
            params["countrycodes"] = country.lower()
        r = requests.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers, timeout=15)
        if r.ok and r.json():
            item = r.json()[0]
            lat, lng = float(item["lat"]), float(item["lon"])
            cache[key] = [lat, lng]
            _save_cache(cache)
            return lat, lng
    except Exception:
        logger.warning("OSM Nominatim geocoding failed for '{}'", query)

    return None
