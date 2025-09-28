try:
    from google.adk import Agent
except Exception:
    Agent = None
from typing import List, Dict, Any, Optional

from .maps_tool import compute_route_tool, MapsToolError
import json
import os


root_agent = None


def create_agent_if_available() -> Optional[Any]:
    """Try to create and return the Agent instance. Returns None on failure or if SDK missing.

    This is lazy so importing this module doesn't attempt to validate Agent constructor args.
    """
    global root_agent
    if root_agent is not None:
        return root_agent
    if Agent is None:
        return None

    # Create the Agent with minimal fields and catch validation errors.
    try:
        root_agent = Agent(
            name="eta_route_agent",
            description="An agent that provides ETA and route info.",
            model="gemini-2.0-flash-001",
        )
        return root_agent
    except Exception as e:
        # don't raise during import; return None and let callers handle missing agent
        print(f"create_agent_if_available: failed to create Agent: {e}")
        root_agent = None
        return None


def _score_from_eta_seconds(eta_seconds: Optional[int]) -> float:
    """Convert ETA (seconds) to a score where higher is better. Handle None safely."""
    if eta_seconds is None:
        return 0.0
    # simple inverse scoring: shorter ETA -> higher score
    return 1.0 / (1.0 + float(eta_seconds))


def select_best_shelter(origin: Dict[str, float], shelters: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Given an origin and list of shelters, compute route to each shelter using
    the backend maps tool, score them, and return the best shelter info.

    Shelter dicts should contain: 'name', 'address', 'lat', 'lng' (lat/lng required).

    Returns a dict: { 'shelter': <shelter dict>, 'eta_seconds': int, 'distance_meters': int, 'polyline': str }
    Raises ValueError if shelters is empty.
    """
    # If no shelters provided, prefer the geocoded dataset if present, otherwise
    # fall back to the raw simulation data and attempt to flatten it.
    if not shelters:
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        geocoded_path = os.path.join(repo_root, 'simulation', 'florida_shelters_geocoded.json')
        sim_path = os.path.join(repo_root, 'simulation', 'florida_shelters.json')

        if os.path.exists(geocoded_path):
            try:
                with open(geocoded_path, 'r', encoding='utf-8') as f:
                    # geocoded file is expected to be a list of shelter dicts
                    shelters = json.load(f)
            except Exception as e:
                raise ValueError(f"failed to load geocoded shelters: {e}")
        else:
            try:
                with open(sim_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                raise ValueError(f"no shelters provided and failed to load simulation data: {e}")

            # simulation file is organized by county -> list of entries
            flattened = []
            for county, entries in data.items():
                for e in entries:
                    name = e.get('name') or e.get('facility') or 'Unnamed'
                    street = e.get('street_address') or e.get('address') or ''
                    address = f"{street}, {county}, FL" if street else f"{county}, FL"
                    item = {'name': name, 'address': address}
                    lat = e.get('lat') or e.get('latitude')
                    lng = e.get('lng') or e.get('longitude')
                    if lat is not None and lng is not None:
                        try:
                            item['lat'] = float(lat)
                            item['lng'] = float(lng)
                        except Exception:
                            pass
                    flattened.append(item)

            shelters = flattened

    results = []
    for s in shelters:
        lat = s.get("lat")
        lng = s.get("lng")
        if lat is None or lng is None:
            # skip entries without coords
            continue
        try:
            # call compute_route_tool with origin -> shelter
            r = compute_route_tool(origin, {"lat": lat, "lng": lng})
        except MapsToolError:
            r = {"distance_meters": None, "duration_seconds": None, "polyline": None}

        # prefer duration_seconds but accept other keys
        eta = r.get("duration_seconds")
        dist = r.get("distance_meters")
        poly = r.get("polyline")

        score = _score_from_eta_seconds(eta)
        results.append({"shelter": s, "eta_seconds": eta, "distance_meters": dist, "polyline": poly, "score": score})

    # sort by score desc, then eta asc
    results.sort(key=lambda x: (-x["score"], (x["eta_seconds"] or float('inf'))))

    if results:
        best = results[0]
        # prepare return shape
        return {
            "shelter": best["shelter"],
            "eta_seconds": best["eta_seconds"],
            "distance_meters": best["distance_meters"],
            "polyline": best["polyline"],
        }
    # If we reached here, there were no geocoded shelters (no lat/lng). Return a sensible fallback.
    if shelters:
        # pick first shelter from the list and return without ETA
        fallback = shelters[0]
        return {
            "shelter": fallback,
            "eta_seconds": None,
            "distance_meters": None,
            "polyline": None,
        }

    raise ValueError("no candidate shelters available")


# Example usage (call this from your orchestration code):
def example_run():
    origin = {"lat": 34.05, "lng": -118.24}
    shelters = [
        {"name": "Shelter A", "address": "123 A St", "lat": 34.07, "lng": -118.25},
        {"name": "Shelter B", "address": "456 B Ave", "lat": 34.03, "lng": -118.22},
    ]
    try:
        best = select_best_shelter(origin, shelters)
        print("Best:", best)
    except Exception as e:
        print("Error selecting shelter:", e)