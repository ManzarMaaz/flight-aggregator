import asyncio
import json
import os
from datetime import datetime, timedelta

import httpx
import redis
from dotenv import load_dotenv
from google import genai
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url

from app import crud
from app.celery_app import celery_app
from app.config import settings
from app.database import SessionLocal
from app.notifications import NotificationManager
from app.schemas import FlightChatRequest, FlightDealVerdict

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

REDIS_HOST = os.getenv("REDIS_HOST", "flight_redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=1, decode_responses=True
)


class AmadeusService:
    """
    Service class to interact with the Amadeus API for flight-related operations,
    including authentication, IATA lookup, and searching for flight deals.
    """

    def __init__(self):
        """Initializes the Amadeus service with configuration settings."""
        self.api_key = settings.AMADEUS_API_KEY
        self.api_secret = settings.AMADEUS_API_SECRET
        self.token_endpoint = settings.TOKEN_ENDPOINT

        self.access_token = None

        self.city_endpoint = settings.CITY_SEARCH_ENDPOINT
        self.flight_endpoint = settings.FLIGHT_ENDPOINT

    async def get_access_token(self):
        """Retrieves a new OAuth access token for Amadeus API authentication."""
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=self.token_endpoint, headers=headers, data=data
                )
                response.raise_for_status()
                token_data = response.json()
                self.access_token = token_data.get("access_token")
                return self.access_token
            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] HTTP error occurred while getting token: {e}")
                return None
            except Exception as e:
                print(f"❌ [SERVICE] An error occurred while getting token: {e}")
                return None

    async def get_iata_code(self, city_name: str):
        """Searches for the 3-letter IATA code for a given city name."""
        if not self.access_token:
            await self.get_access_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"keyword": city_name, "max": "1"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=self.city_endpoint, params=params, headers=headers
                )
                response.raise_for_status()
                data = response.json().get("data", [])
                if data and "iataCode" in data[0]:
                    return data[0]["iataCode"]
                return None

            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] Error during City Search API call: {e}")
                return None

    async def check_flights(
        self,
        origin_code,
        destination_code,
        departure_date,
        arrival_date,
        is_direct=True,
    ):
        """
        Searches for the cheapest flight price for the given route and date.

        Returns:
            tuple or None: A tuple (price_str, stops_count) if a flight is found,
                           or None if no flight is found.
        """
        if not self.access_token:
            await self.get_access_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}

        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": departure_date.strftime("%Y-%m-%d"),
            "returnDate": arrival_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": "INR",
            "max": "1",
            "nonStop": "true" if is_direct else "false",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=self.flight_endpoint, headers=headers, params=query
                )
                response.raise_for_status()
                result = response.json()

                if result.get("data") and len(result["data"]) > 0:
                    flight_data = result["data"][0]
                    total_price = flight_data["price"]["grandTotal"]
                    stops = len(flight_data["itineraries"][0]["segments"]) - 1
                    return total_price, stops
                return None

            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] Error during Flight Offers API call: {e}")
                return None


async def track_flights_deals(
    origin: str, days_in_advance: int, search_windows_days: int
):
    """
    Background task logic to track and notify about flight deals.
    """
    amadeus_service = AmadeusService()
    notification_manager = NotificationManager()

    departure_date = datetime.now() + timedelta(days=days_in_advance)
    arrival_date = departure_date + timedelta(days=search_windows_days)

    db = SessionLocal()

    try:
        destinations = crud.get_active_destinations(db)
        results = []

        for dest in destinations:
            if not dest.iata_code:
                continue

            flight_result = await amadeus_service.check_flights(
                origin_code=origin,
                destination_code=dest.iata_code,
                departure_date=departure_date,
                arrival_date=arrival_date,
                is_direct=True,
            )

            if flight_result:
                price, stops = flight_result

                if float(price) < dest.target_price:
                    results.append(
                        {
                            "city": dest.city_name,
                            "iata_code": dest.iata_code,
                            "target_price": dest.target_price,
                            "current_price": price,
                            "stops": stops,
                        }
                    )
                    message_body = f"Flight deal alert! {dest.city_name} ({dest.iata_code}) is now ₹{price}, below your target of ₹{dest.target_price}."
                    notification_manager.send_email(
                        subject="Flight Deal Alert!",
                        body=message_body,
                        to_email=settings.MY_MAIL,
                    )
                    notification_manager.send_sms(message_body)

            await asyncio.sleep(2)
        return results
    finally:
        db.close()


@celery_app.task(name="app.services.celery_track_flights")
def celery_track_flights(origin: str, days_in_advance: int, search_windows_days: int):
    """
    Celery task wrapper for triggering flight deal tracking.
    """
    results = asyncio.run(
        track_flights_deals(origin, days_in_advance, search_windows_days)
    )
    return results


@celery_app.task
def analyze_flight_deal_task(origin: str, destination: str, price: int):
    """
    Analyzes flight deal using structured Gemini output to prevent JSON hallucinations.
    """
    cache_key = (
        f"flight_deal:{origin.strip().lower()}:{destination.strip().lower()}:{price}"
    )

    # 1. Define the Pydantic model for the schema
    # (Assuming FlightDealVerdict is already defined in schemas.py as the target structure)

    # 2. Call Gemini with response_schema
    try:
        prompt = f"Analyze this deal: Origin: {origin}, Destination: {destination}, Price: {price}"

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=FlightDealVerdict,
            ),
        )

        # 3. Parse result
        verdict = FlightDealVerdict.model_validate_json(response.text)

        # 4. Cache and return
        redis_client.setex(cache_key, 86400, verdict.model_dump_json())
        return verdict.model_dump()

    except Exception as e:
        print(f"[Worker] AI Pipeline Error: {e}")
        return {"error": "AI failed to return the guaranteed schema."}


def process_flight_chat(request: FlightChatRequest):
    """
    Handles multi-turn chat interactions to gather flight search requirements.
    """
    system_prompt = """You are a helpful flight deal assistant.
    Your goal is to gather exactly 3 pieces of information from the user:
    1. Origin City
    2. Destination City
    3. Target Price Budget

    RULES:
    - If you are missing ANY of these 3 pieces of information, ask the user for them.
    - If you have ALL 3 pieces, output ONLY a raw JSON object matching this exact schema:
      {"origin_iata": "JFK", "destination_iata": "LHR", "is_good_deal": true, "reasoning": "..."}
    """

    formatted_history = []
    formatted_history.append({"role": "user", "parts": [system_prompt]})
    formatted_history.append(
        {"role": "model", "parts": ["Understood. I will follow the rules."]}
    )

    for turn in request.chat_history:
        formatted_history.append({"role": turn.role, "parts": [turn.text]})

    formatted_history.append({"role": "user", "parts": [request.new_message]})

    try:
        # Assuming you want to use the 'client' initialized at module level
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",  # Changed model to a standard one
            contents=formatted_history,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
            ),
        )

        raw_text = response.text.strip()

        if raw_text.startswith("{") and raw_text.endswith("}"):
            try:
                parsed_json = json.loads(raw_text)
                return {"type": "analysis_complete", "data": parsed_json}
            except json.JSONDecodeError:
                return {"type": "chat_response", "text": raw_text}
        else:
            return {"type": "chat_response", "text": raw_text}

    except Exception as e:
        print(f"[API] Gemini Chat Error: {e}")
        return {
            "type": "error",
            "message": "The AI encountered an error processing your request.",
        }


class RAGService:
    _query_engine = None

    @classmethod
    def initialize(cls):
        """Called once during FastAPI startup."""
        print("[System] Booting up RAG Engine...")
        # TODO: Setup Settings.llm and Settings.embed_model
        Settings.llm = GoogleGenAI(
            model="gemini-2.5-flash-lite", api_key=os.getenv("GEMINI_API_KEY")
        )
        Settings.embed_model = GoogleGenAIEmbedding(
            model_name="gemini-embedding-2", api_key=os.getenv("GEMINI_API_KEY")
        )

        url = make_url(DATABASE_URL)
        vector_store = PGVectorStore.from_params(
            database=url.database,
            host=url.host,
            password=url.password,
            port=url.port,
            user=url.username,
            table_name="data_flight_policy",
            embed_dim=3072,
        )

        index = VectorStoreIndex.from_vector_store(vector_store)

        cls._query_engine = index.as_query_engine(similarity_top_k=3)

    @classmethod
    async def ask_policy(cls, question: str):
        """Called by the router on every request."""
        if cls._query_engine is None:
            raise ValueError("RAG Engine not initialized")

        return cls._query_engine.query(question)
