from datetime import datetime, timedelta

from app.config import settings
import httpx
from app.database import SessionLocal
from app import crud
from app.notifications import NotificationManager

class AmadeusService:

    def __init__(self):
        print("🔧 [SERVICE] Initializing AmadeusService...")
        self.api_key = settings.AMADEUS_API_KEY
        self.api_secret = settings.AMADEUS_API_SECRET
        self.token_endpoint = settings.TOKEN_ENDPOINT

        self.access_token = None

        self.city_endpoint = settings.CITY_SEARCH_ENDPOINT
        self.flight_endpoint = settings.FLIGHT_ENDPOINT
        print("✅ [SERVICE] AmadeusService initialized.")

    async def get_access_token(self):
        print("🔐 [SERVICE] Requesting Amadeus access token...")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url=self.token_endpoint, headers=headers, data=data)
                response.raise_for_status()
                print("✅ [SERVICE] Token acquired successfully.")
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                return self.access_token
            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] HTTP error occurred while getting token: {e}")
                return None
            except Exception as e:
                print(f"❌ [SERVICE] An error occurred while getting token: {e}")
                return None
            
    async def get_iata_code(self, city_name: str):
        """
        Searches for the 3-letter IATA code for a given city name.
        """
        print(f"\n🔍 [SERVICE] Searching IATA code for: {city_name}")
        if not self.access_token:
            await self.get_access_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {'keyword': city_name, 'max': '1'}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=self.city_endpoint, params=params, headers=headers)
                response.raise_for_status()
                data = response.json().get('data', [])
                if data and 'iataCode' in data[0]:
                    iata_code = data[0]['iataCode']
                    print(f"✅ [SERVICE] IATA code found for {city_name}: {iata_code}")
                    return iata_code
                print(f"❌ [SERVICE] No IATA code found for {city_name}")
                return None
                
            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] Error during City Search API call: {e}")
                return None

    async def check_flights(self, origin_code, destination_code, departure_date, arrival_date, is_direct=True):
        """
        Searches for the cheapest flight price for the given route and date.
        
        Returns:
            tuple or None: A tuple (price_str, stops_count) if a flight is found, 
                           or None if no flight is found.
        """
        flight_type = "Direct" if is_direct else "Indirect"
        print(f"\n✈️  [SERVICE] Searching {flight_type} flights: {origin_code} → {destination_code} ({departure_date} to {arrival_date})")
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
            "nonStop": "true" if is_direct else "false" 
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url=self.flight_endpoint, headers=headers, params=query)
                response.raise_for_status()
                result = response.json()

                if result.get('data') and len(result['data']) > 0:
                    flight_data = result['data'][0]
                    total_price = flight_data['price']['grandTotal']
                    
                    # Number of stops = (Number of segments) - 1
                    stops = len(flight_data['itineraries'][0]['segments']) - 1
                    print(f"✅ [SERVICE] {flight_type} flight found: ₹{total_price} with {stops} stop(s)")
                    return total_price, stops
                print(f"❌ [SERVICE] No {flight_type} flights found for {destination_code}")
                return None
            
            except httpx.HTTPError as e:
                print(f"❌ [SERVICE] Error during Flight Offers API call: {e}")
                return None
            
async def track_flights_deals(origin: str, days_in_advance: int, search_windows_days: int):
    print("\n\n🚀 [BACKGROUND_TASK] Flight tracking started")
    print(f"   Origin: {origin}")
    print(f"   Days in advance: {days_in_advance}")
    print(f"   Search window: {search_windows_days} days")
    
    amadeus_service = AmadeusService()
    notification_manager = NotificationManager()
    
    departure_date = datetime.now() + timedelta(days=days_in_advance)
    arrival_date = departure_date + timedelta(days=search_windows_days)
    print(f"   Departure: {departure_date.date()}, Arrival: {arrival_date.date()}\n")

    db = SessionLocal()

    try:
        print("📄 [BACKGROUND_TASK] Fetching destinations from database...")
        destinations = crud.get_active_destinations(db)
        results = []

        for idx, dest in enumerate(destinations, 1):
            print(f"\n[{idx}/{len(destinations)}] Processing {dest.city_name}...")
            if not dest.iata_code:
                print(f"   ❌ Skipping {dest.city_name}: Missing IATA code.")
                continue

            flight_result = await amadeus_service.check_flights(
                origin_code=origin,
                destination_code=dest.iata_code,
                departure_date=departure_date,
                arrival_date=arrival_date,
                is_direct=True
            )

            if flight_result:
                price, stops = flight_result
                print(f"   Price: ₹{price}, Target: ₹{dest.target_price}")

                if float(price) < dest.target_price:
                    results.append({
                        "city": dest.city_name,
                        "iata_code": dest.iata_code,
                        "target_price": dest.target_price,
                        "current_price": price,
                        "stops": stops
                    })
                    print(f"   🌟 DEAL FOUND for {dest.city_name}! Price: ₹{price} (Target: ₹{dest.target_price})")
                   
                    # Send notifications
                    message_body = f"Flight deal alert! {dest.city_name} ({dest.iata_code}) is now ₹{price}, below your target of ₹{dest.target_price}."
                    notification_manager.send_email(
                        subject="Flight Deal Alert!",
                        body=message_body,
                        to_email=settings.MY_MAIL
                    )
                    notification_manager.send_sms(message_body)
                else:
                    print("   ℹ️  Price above target. No alert.")
            else:
                print("   ❌ No flights found.")
        
        print(f"\n\n✅ [BACKGROUND_TASK] Flight tracking completed. Found {len(results)} deal(s).\n")
        return results
    finally:
        db.close()
        print("[BACKGROUND_TASK] Database connection closed.")