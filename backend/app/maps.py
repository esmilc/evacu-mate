import os
from typing import Dict, Any
import requests

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def _make_compute_routes_payload(origin: Dict[str, float], dest: Dict[str, float]) -> Dict[str, Any]:
    return {
        "origin": {"location": {"latLng": {"latitude": origin["lat"], "longitude": origin["lng"]}}},
        "destination": {"location": {"latLng": {"latitude": dest["lat"], "longitude": dest["lng"]}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternatives": False,
    }


def compute_route(origin: Dict[str, float], dest: Dict[str, float]) -> Dict[str, Any]:
    """Call the Google Routes API computeRoutes endpoint and return parsed summary.

    Returns a dict with: distance_meters, duration_seconds, polyline (encoded), raw (full response).
    """
    if API_KEY is None:
        raise RuntimeError("GOOGLE_MAPS_API_KEY not set in environment")

    url = f"https://routes.googleapis.com/directions/v2:computeRoutes?key={API_KEY}"
    payload = _make_compute_routes_payload(origin, dest)
    resp = requests.post(url, json=payload, timeout=10)
    resp.raise_for_status()
    j = resp.json()

    routes = j.get("routes") or []
    if not routes:
        return {"distance_meters": None, "duration_seconds": None, "polyline": None, "raw": j}

    # take first route
    route = routes[0]
    distance = 0
    duration = 0
    for leg in route.get("legs", []):
        distance += leg.get("distanceMeters", 0) or 0
        # duration may be a dict or a number depending on API; try a few keys
        d = leg.get("duration") or leg.get("travelTime") or {}
        if isinstance(d, dict):
            duration += d.get("seconds", 0) or 0
        elif isinstance(d, (int, float)):
            duration += int(d)

    polyline = route.get("polyline", {}).get("encodedPolyline") or route.get("polyline", {}).get("points")

    return {
        "distance_meters": distance,
        "duration_seconds": duration,
        "polyline": polyline,
        "raw": j,
    }
