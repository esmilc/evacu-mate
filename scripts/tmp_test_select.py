from agents.eta_route_agent import agent as a
import json

def _stub(origin, destination, retries=1, timeout=6.0):
    dlat = abs(origin['lat'] - destination['lat'])
    eta = int(dlat * 10000)
    return {'distance_meters': int(eta*10), 'duration_seconds': eta, 'polyline': 'stub'}

# Monkey-patch
a.compute_route_tool = _stub

origin = {'lat': 27.6648, 'lng': -81.5158}
shelters = [
    {'name': 'Shelter A', 'address': 'A', 'lat': 27.7, 'lng': -81.5},
    {'name': 'Shelter B', 'address': 'B', 'lat': 28.0, 'lng': -81.6},
    {'name': 'Shelter C', 'address': 'C', 'lat': 27.66, 'lng': -81.52},
]

print('Running quick select_best_shelter test...')
res = a.select_best_shelter(origin, shelters)
print(json.dumps(res, indent=2))
