import requests
import json
import sys

API_URL = "http://127.0.0.1:8000/api/v1/flights/chat"

def run_flight_agent():
    """
    Main entry point for the command-line client to interact with the flight deal assistant API.
    """
    print("DEBUG: Starting AI Flight Deal Analyst.")
    print("INFO: Welcome to the AI Flight Deal Analyst.")
    print("INFO: Type 'exit' or 'quit' to close the terminal.\n")
    print("INFO: AI: Hello! Where are you looking to fly out of?")

    chat_history = []

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("INFO: Ending session.")
                break

            if not user_input.strip():
                continue

            payload = {
                "chat_history": chat_history,
                "new_message": user_input
            }

            print(f"DEBUG: Sending request to {API_URL} with payload: {payload}")
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG: Received response: {data}")

                if data.get("type") == "chat_response":
                    ai_text = data.get("text")
                    print(f"\nAI: {ai_text}")

                    chat_history.append({"role": "user", "text": user_input})
                    chat_history.append({"role": "model", "text": ai_text})

                elif data.get("type") == "analysis_complete":
                    print("\n✅ [API RETURNED FINAL JSON DATA]")

                    final_data = data.get("data", {})
                    print(json.dumps(final_data, indent=2))

                    print("\nINFO: Workflow complete. Resetting memory for a new search...")
                    chat_history = []

                elif data.get("type") == "error":
                    print(f"\n🚨 API Error: {data.get('message')}")

            else:
                print(f"\n🚨 Server Error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n🚨 CRITICAL: Cannot connect to server. Is FastAPI running on port 8000?")
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nINFO: Ending session.")
            break

if __name__ == "__main__":
    run_flight_agent()
