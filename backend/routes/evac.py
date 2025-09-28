# backend/routes/evac.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
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
    # shelters optional: if not provided, agent will load simulation/florida_shelters.json
    shelters: Optional[List[Shelter]] = None

@router.post("/best-shelter")
def get_best_shelter(body: RequestBody):
    try:
        # expose received payload for debugging
        payload = body.dict()
        print('GET /best-shelter payload:', payload)
        shelters = [s.dict() for s in body.shelters] if body.shelters else []
        best = select_best_shelter(body.origin.dict(), shelters)
        return {"best": best, "payload": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))