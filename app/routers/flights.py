from fastapi import APIRouter, BackgroundTasks
import redis
import json
from app.schemas import FlightTrackRequest, FlightChatRequest, FlightDealRequest
from app.services import track_flights_deals, process_flight_chat, analyze_flight_deal_task

router = APIRouter(prefix="/flights", tags=["Flights"])

redis_client = redis.Redis(host='localhost', port=6379, db=1, decode_responses=True)

@router.post("/track-flights")
def track_flights(request: FlightTrackRequest, background_tasks: BackgroundTasks):
    """
    Triggers a background task to track flight prices for a given origin.
    """
    print(f"INFO: Tracking flights started from {request.origin_iata}.")
    background_tasks.add_task(
        track_flights_deals,
        request.origin_iata,
        request.days_in_advance,
        request.search_windows_days,
    )
    return {
        "message": "Flight tracking initiated.",
        "origin": request.origin_iata,
    }

@router.post("/analyze-deal")
async def analyze_deal(request: FlightDealRequest):
    """
    Analyzes whether a provided flight deal meets target pricing criteria using AI.
    """
    cache_key = f"flight_deal:{request.origin_city.strip().lower()}:{request.destination_city.strip().lower()}:{request.target_price}"

    cached_data = redis_client.get(cache_key)

    if cached_data:
        print(f"INFO: Cache hit for {cache_key}")
        return {"status": "success", "source": "redis_cache", "data": json.loads(cached_data)}

    print(f"INFO: Cache miss. Sending to Celery for {cache_key}")

    task = analyze_flight_deal_task.delay(
        request.origin_city,
        request.destination_city,
        request.target_price
    )

    return {
        "status": "processing",
        "source": "ai_worker",
        "task_id": task.id
    }

@router.post("/chat")
async def chat_with_agent(request: FlightChatRequest):
    """
    Handles conversational interactions with the AI flight assistant.
    """
    print("INFO: Chat agent request received.")
    response = process_flight_chat(request)
    return response
