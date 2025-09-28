'''
Ensure necessary indexes exist in the database.
'''
from .client import get_db
from .collections import COLL

def ensure_indexes():
    db = get_db()
    try:
        db[COLL["hazards"]].create_index([("geom", "2dsphere")])
        db[COLL["zones"]].create_index([("geom", "2dsphere")])
        db[COLL["shelters"]].create_index([("loc", "2dsphere")])
        db[COLL["requests"]].create_index([("loc", "2dsphere")])
        db[COLL["requests"]].create_index([("status", 1), ("created_at", 1)])
        db[COLL["vehicles"]].create_index([("loc", "2dsphere"), ("status", 1)])
        db[COLL["dispatches"]].create_index([("vehicle_id", 1), ("status", 1)])
        db[COLL["telemetry"]].create_index("ts", expireAfterSeconds=72*3600)
    except Exception as e:
        # Non-fatal in development: log the error and continue so server can start
        print(f"ensure_indexes: warning, failed to ensure indexes (continuing): {e}")