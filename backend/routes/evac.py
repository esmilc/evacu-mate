# backend/routes/evac.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from agents.eta_route_agent.agent import select_best_shelter

router = APIRouter()

class Shelter(BaseModel):
    name: str
    address: str
    lat: float
    lng: float

class Origin(BaseModel):
    lat: float
    lng: float

class RequestBody(BaseModel):
    origin: Origin
    shelters: List[Shelter]

@router.post("/best-shelter")
def get_best_shelter(body: RequestBody):
    try:
        best = select_best_shelter(body.origin.dict(), [s.dict() for s in body.shelters])
        return {"best": best}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))