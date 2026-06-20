import requests

class FlightSearch:
    """
    Handles all communication with the Amadeus API, covering authentication,
    IATA code lookups, and searching for the cheapest available flights.
    """
    def __init__(self, api_key, api_secret, token_endpoint, city_endpoint, flight_endpoint):
        """
        Initializes the service with API credentials and endpoints, then authenticates immediately.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_endpoint = token_endpoint
        self.city_endpoint = city_endpoint
        self.flight_endpoint = flight_endpoint

        self.access_token = self._get_new_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def _get_new_token(self):
        """
        Requests a new OAuth access token from Amadeus using client credentials.
        """
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.api_secret
        }
        try:
            response = requests.post(url=self.token_endpoint, headers=header, data=body)
            response.raise_for_status()
            print(f"DEBUG: Token response status: {response.status_code}")
            return response.json()['access_token']
        except requests.exceptions.RequestException as e:
            print(f"CRITICAL: Error getting Amadeus token: {e}")
            return None

    def get_iata_code(self, city_name: str):
        """
        Finds the 3-letter IATA airport code for a specified city name.
        """
        city_params = {'keyword': city_name, 'max': '1'}
        try:
            response = requests.get(url=self.city_endpoint, params=city_params, headers=self.headers)
            response.raise_for_status()
            data = response.json().get('data', [])
            if data and 'iataCode' in data[0]:
                print(f"INFO: IATA code for {city_name} found: {data[0]['iataCode']}")
                return data[0]['iataCode']
            else:
                print(f"WARN: IATA code not found for {city_name}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: City Search API call failed: {e}")
            return None

    def check_flights(self, origin_code, destination_code, departure_date, arrival_date, is_direct=True):
        """
        Queries the Amadeus API for the cheapest flight price on a specific route.

        Returns:
            tuple: (price, stops_count) if found, otherwise None.
        """
        non_stop_param = "true" if is_direct else "false"
        currency = "INR"

        query = {
            "originLocationCode": origin_code,
            "destinationLocationCode": destination_code,
            "departureDate": departure_date.strftime("%Y-%m-%d"),
            "returnDate": arrival_date.strftime("%Y-%m-%d"),
            "adults": 1,
            "currencyCode": currency,
            "max": "1",
            "nonStop": non_stop_param
        }

        try:
            response = requests.get(url=self.flight_endpoint, headers=self.headers, params=query)
            response.raise_for_status()
            result = response.json()

            if result.get('data') and len(result['data']) > 0:
                flight_data = result['data'][0]
                total_price = flight_data['price']['grandTotal']

                stops = len(flight_data['itineraries'][0]['segments']) - 1
                print(f"INFO: Found flight from {origin_code} to {destination_code} at {total_price} {currency} with {stops} stops.")

                return total_price, stops
            else:
                print(f"INFO: No flights found for {origin_code} to {destination_code} on {departure_date}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Flight Offers API call failed: {e}")
            return None
