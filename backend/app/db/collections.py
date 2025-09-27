'''
Here lies the collections that are used in the database.
'''

COLL = {
    "hazards": "hazards", # Collection for storing hazard zones, so the system knows where not to go using polygons.
    "zones": "zones", #defines city regions and their evacuation priority scores.
    "shelters": "shelters", #safe drop-off points with capacity tracking.
    "requests": "requests",  #evacuee pickup requests from users.
    "vehicles": "vehicles", #the fleet of autonomous cars with status and capacity.
    "dispatches": "dispatches", #planned assignments of vehicles to requests and shelters.
    "telemetry": "telemetry" #live vehicle location and occupancy updates for the map.
}