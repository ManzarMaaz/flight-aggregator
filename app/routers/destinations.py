from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import DestinationCreate, DestinationResponse

router = APIRouter(prefix="/destinations", tags=["Flight Destinations"])


@router.post("/create", response_model=DestinationResponse)
def create_destination(destination: DestinationCreate, db: Session = Depends(get_db)):
    print("\n🚀 [ENDPOINT] POST /api/v1/destinations - Creating destination")
    db_destination = crud.create_destination(db, destination)
    print("✅ [ENDPOINT] Destination endpoint completed\n")
    return db_destination


@router.get("/list/", response_model=list[DestinationResponse])
def list_destinations(db: Session = Depends(get_db)):
    print("\n🚀 [ENDPOINT] GET /api/v1/destinations/list - Listing destinations")
    destinations = crud.list_destinations(db)
    print("✅ [ENDPOINT] List destinations endpoint completed\n")
    return destinations


@router.post("/delete/{destination_id}")
def delete_specific_destination(destination_id: int, db: Session = Depends(get_db)):
    print(
        f"\n🚀 [ENDPOINT] POST /api/v1/destinations/delete/{destination_id} - Deleting destination"
    )
    crud.delete_specific_destination(db, destination_id)
    print("✅ [ENDPOINT] Delete destination endpoint completed\n")
    return {"message": f"Destination with ID {destination_id} deleted successfully."}


@router.post("/delete-all")
def delete_all_destinations(db: Session = Depends(get_db)):
    print(
        "\n🚀 [ENDPOINT] POST /api/v1/destinations/delete-all - Deleting all destinations"
    )
    crud.delete_all_destinations(db)
    print("✅ [ENDPOINT] Delete all destinations endpoint completed\n")
    return {"message": "All destinations deleted successfully."}
