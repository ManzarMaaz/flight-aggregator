# 1. Standard Library & Environment
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.database import Base, engine
from app.routers import destinations, flights, policies, users
from app.services import RAGService

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        RAGService.initialize()
    except Exception as e:
        print(f"Failed to load RAG DB: {e}")
    yield
    print("Shutting down...")


app = FastAPI(title="Flight Aggregator API", version="2.0.0", lifespan=lifespan)

app.include_router(policies.router)
app.include_router(flights.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(destinations.router, prefix="/api/v1")


@app.get("/")
def health_check():
    """
    Simple health check endpoint to verify the API is running.
    """
    print("INFO: Health check endpoint accessed.")
    return {"status": "ok", "message": "Flight Aggregator API is running!"}
