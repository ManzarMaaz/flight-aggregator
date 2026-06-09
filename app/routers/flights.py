from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import FlightTrackRequest, DestinationResponse, DestinationCreate
from app.services import track_flights_deals
from app import crud
from app.services import AmadeusService

router = APIRouter(tags=["Flight Tracking"])

@router.post("/track-flights")
def track_flights(request: FlightTrackRequest, background_tasks: BackgroundTasks):
    print(f"\n🚀 [ENDPOINT] POST /api/v1/track-flights - Flight tracking started")
    print(f"   Origin: {request.origin_iata}")
    print(f"   Days in advance: {request.days_in_advance}")
    print(f"   Search window: {request.search_windows_days} days")
    background_tasks.add_task(track_flights_deals, request.origin_iata, request.days_in_advance, request.search_windows_days)
    print("✅ [ENDPOINT] Background task queued for flight tracking\n")
    return {"message": "Flight tracking initiated. Results will be printed in the console.",
    "origin": request.origin_iata,
    }

@router.post("/destinations", response_model=DestinationResponse)
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    print(f"\n🚀 [ENDPOINT] POST /api/v1/destinations - Creating destination")
    db_destination = crud.create_destination(db, destination)
    print("✅ [ENDPOINT] Destination endpoint completed\n")
    return db_destination