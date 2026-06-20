from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class FlightTrackRequest(BaseModel):
    origin_iata: str = "HYD"
    days_in_advance: int = 1
    search_windows_days: int = 30


class FlightDealResponse(BaseModel):
    city_name: str
    iata_code: str
    target_price: float
    cheapest_price: Optional[float] = None
    row_id: Optional[int] = None
    stops: int = 0


class DestinationCreate(BaseModel):
    city_name: str
    iata_code: Optional[str] = None
    target_price: float


class DestinationResponse(DestinationCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserResponse(UserCreate):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class FlightDealRequest(BaseModel):
    origin_city: str = Field(..., json_schema_extra={"example": "City"})
    destination_city: str = Field(..., json_schema_extra={"example": "City"})
    target_price: int = Field(..., json_schema_extra={"example": "City"})


class FlightDealVerdict(BaseModel):
    origin_iata: str
    destination_iata: str
    is_good_deal: bool
    reasoning: str


class ChatTurn(BaseModel):
    role: str = Field(..., description="'user' or 'model'")
    text: str


class FlightChatRequest(BaseModel):
    chat_history: List[ChatTurn] = []
    new_message: str


class PolicyRequest(BaseModel):
    question: str


class Citation(BaseModel):
    source_text: str
    relevance_score: float


class PolicyResponse(BaseModel):
    answer: str
    citations: List[Citation]
