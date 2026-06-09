from fastapi import APIRouter, BackgroundTasks

from app.schemas import FlightTrackRequest
from app.services import track_flights_deals

router = APIRouter(tags=["Flight Tracking"])


@router.post("/track-flights")
def track_flights(request: FlightTrackRequest, background_tasks: BackgroundTasks):
    print("\n🚀 [ENDPOINT] POST /api/v1/track-flights - Flight tracking started")
    print(f"   Origin: {request.origin_iata}")
    print(f"   Days in advance: {request.days_in_advance}")
    print(f"   Search window: {request.search_windows_days} days")
    background_tasks.add_task(
        track_flights_deals,
        request.origin_iata,
        request.days_in_advance,
        request.search_windows_days,
    )
    print("✅ [ENDPOINT] Background task queued for flight tracking\n")
    return {
        "message": "Flight tracking initiated. Results will be printed in the console.",
        "origin": request.origin_iata,
    }
