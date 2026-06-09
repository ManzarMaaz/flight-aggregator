from pydantic import BaseModel
from typing import Optional

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
    id : int
    is_active: bool

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserResponse(UserCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True