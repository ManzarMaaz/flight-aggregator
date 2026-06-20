import requests

class FlightDataManager:
    """
    Manages communication with an external Google Sheet (using Sheety)
    to track destination preferences and user contact information.
    """
    def __init__(self, prices_endpoint, users_endpoint, username, password):
        """
        Sets up the manager with Sheety API endpoints and authentication credentials.
        """
        self.prices_endpoint = prices_endpoint
        self.users_endpoint = users_endpoint
        self.auth = (username, password)

    def get_destination_data(self):
        """
        Retrieves a list of all target destinations from the Google Sheet.
        """
        try:
            response = requests.get(url=self.prices_endpoint, auth=self.auth)
            response.raise_for_status()
            data = response.json().get('prices', [])
            print(f"INFO: Fetched {len(data)} destinations from Sheety.")
            return data
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error fetching prices data from Sheety: {e}")
            return []

    def get_customer_emails(self):
        """
        Fetches the contact details for all registered users from the sheet.
        """
        try:
            response = requests.get(url=self.users_endpoint, auth=self.auth)
            response.raise_for_status()
            data = response.json().get('users', [])
            print(f"INFO: Fetched {len(data)} customers from Sheety.")
            return data
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error fetching customer data from Sheety: {e}")
            return []

    def update_iata_code(self, row_id: int, iata_code: str):
        """
        Updates the IATA code for a specific destination row in the Google Sheet.
        """
        sheety_updated_url = f"{self.prices_endpoint}/{row_id}"
        body = {
            'price': {
                'iataCode': iata_code
            }
        }
        try:
            response = requests.put(
                url=sheety_updated_url,
                json=body,
                auth=self.auth
            )
            response.raise_for_status()
            print(f"INFO: Updated row {row_id} with IATA code {iata_code}.")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Error updating IATA code in Sheety for row {row_id}: {e}")
