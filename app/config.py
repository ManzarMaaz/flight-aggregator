from pydantic_settings import BaseSettings, SettingsConfigDict

print("\n🔧 [CONFIG] Loading environment variables...")

class Settings(BaseSettings):
    # Amadeus API
    AMADEUS_API_KEY: str
    AMADEUS_API_SECRET: str
    TOKEN_ENDPOINT: str
    CITY_SEARCH_ENDPOINT: str
    FLIGHT_ENDPOINT: str

    # PostgreSQL Database
    DATABASE_URL: str

    # Twilio & Email
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_VIRTUAL_NUMBER: str
    TWILIO_VERIFIED_NUMBER: str

    # Email credentials
    MY_MAIL: str
    MY_PASS: str
    SMTP_SERVER: str
    

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
print("✅ [CONFIG] Environment variables loaded successfully.\n")