from fastapi import FastAPI

from app.database import Base, engine
from app.routers import destinations, flights, users

print("\n🚀 [STARTUP] Initializing database tables...")
Base.metadata.create_all(bind=engine)
print("✅ [STARTUP] Database tables created/verified.\n")

app = FastAPI(
    title="Flight Aggregator API",
    description="High-performance asynchronous API for tracking flight deals and managing users.",
    version="2.0.0",
)

print("🚀 [STARTUP] Registering routers...")
# Register routers
app.include_router(flights.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(destinations.router, prefix="/api/v1")
print("✅ [STARTUP] Routers registered successfully.\n")


@app.get("/")
def health_check():
    print("🔍 [ENDPOINT] GET / - Health check requested.")
    return {"status": "ok", "message": "Flight Aggregator API is running!"}
