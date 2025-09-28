from fastapi import FastAPI # type: ignore
from app.db.ensure_indexes import ensure_indexes
from app.db.client import get_db
from app.db.collections import COLL
from app.maps import compute_route

app = FastAPI()

@app.on_event("startup")
def startup():
    ensure_indexes()

@app.post("/user/requests")
def create_request(req: dict):
    db = get_db()
    req["status"] = "pending"
    req["created_at"] = req.get("created_at")
    db[COLL["requests"]].insert_one(req)
    return {"ok": True}


@app.post("/compute-route")
def compute_route_endpoint(payload: dict):
    """Payload: {"origin": {"lat": float, "lng": float}, "destination": {"lat": float, "lng": float}}"""
    origin = payload.get("origin")
    dest = payload.get("destination")
    if not origin or not dest:
        return {"error": "origin and destination required"}
    try:
        res = compute_route(origin, dest)
        return res
    except Exception as e:
        return {"error": str(e)}