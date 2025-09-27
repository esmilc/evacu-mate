from fastapi import FastAPI # type: ignore
from app.db.ensure_indexes import ensure_indexes
from app.db.client import get_db
from app.db.collections import COLL

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