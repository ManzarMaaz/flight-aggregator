from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import DestinationCreate, DestinationResponse

router = APIRouter(prefix="/destinations", tags=["Flight Destinations"])


@router.post("/create", response_model=DestinationResponse)
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    """
    Registers a new destination for flight tracking.
    """
    print(f"INFO: Creating destination: {destination.city_name}")
    db_destination = crud.create_destination(db, destination)
    return db_destination


@router.get("/list/", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    """
    Returns a list of all currently registered tracking destinations.
    """
    print("INFO: Fetching destination list.")
    destinations = crud.list_destinations(db)
    return destinations


@router.post("/delete/{destination_id}")
def delete_specific_destination(destination_id: int, db: Session = Depends(get_db)):
    """
    Removes a specific destination from the tracking list.
    """
    print(f"INFO: Deleting destination ID: {destination_id}")
    crud.delete_specific_destination(db, destination_id)
    return {"message": f"Destination with ID {destination_id} deleted successfully."}


@router.post("/delete-all")
def delete_all_destinations(db: Session = Depends(get_db)):
    """
    Removes all tracking destinations from the system.
    """
    print("INFO: Deleting all destinations.")
    crud.delete_all_destinations(db)
    return {"message": "All destinations deleted successfully."}
