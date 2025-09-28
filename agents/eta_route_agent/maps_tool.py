import os
import time
from typing import Dict, Any

import requests

# Backend endpoint (adjust host/port in env or fallback to localhost)
BACKEND_URL = os.getenv("EVACU_BACKEND_URL", "http://localhost:8000")
COMPUTE_ROUTE_PATH = "/compute-route"


class MapsToolError(RuntimeError):
    pass


def compute_route_tool(origin: Dict[str, float], destination: Dict[str, float], retries: int = 1, timeout: float = 6.0) -> Dict[str, Any]:
    """Call the backend /compute-route endpoint and return parsed result.

    origin/destination: {"lat": float, "lng": float}
    Returns the backend response (distance_meters, duration_seconds, polyline, raw)
    Raises MapsToolError on failure.
    """
    if not origin or not destination:
        raise MapsToolError("origin and destination required")

    url = BACKEND_URL.rstrip("/") + COMPUTE_ROUTE_PATH
    payload = {"origin": origin, "destination": destination}

    attempt = 0
    while True:
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and data.get("error"):
                raise MapsToolError(f"backend error: {data.get('error')}")
            return data
        except requests.RequestException as e:
            attempt += 1
            if attempt > retries:
                raise MapsToolError(f"request failed after {attempt} attempts: {e}") from e
            time.sleep(0.5)
