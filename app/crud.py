import os

from sqlalchemy.orm import Session

from app import models, schemas
from flight_search import FlightSearch


# Helper to initialize the FlightSearch service
def get_flight_search_service():
    return FlightSearch(
        api_key=os.getenv("AMADEUS_API_KEY"),
        api_secret=os.getenv("AMADEUS_API_SECRET"),
        token_endpoint=os.getenv("TOKEN_ENDPOINT"),
        city_endpoint=os.getenv("CITY_SEARCH_ENDPOINT"),
        flight_endpoint=os.getenv("FLIGHT_ENDPOINT"),
    )


def create_user(db: Session, user: schemas.UserCreate):
    """
    Persists a new user into the database and returns the created user record.
    """
    db_user = models.User(**user.model_dump())
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        print(f"INFO: User created with ID: {db_user.id}")
        return db_user
    except Exception as e:
        db.rollback()
        print(f"ERROR: Database error during user creation: {e}")
        raise


def get_user_by_email(db: Session, email: str):
    """
    Looks up a user record in the database using their email address.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        print(f"INFO: User found: ID={user.id}")
    return user


def create_destination(db: Session, destination: schemas.DestinationCreate):
    """
    Saves a new flight destination to the database for tracking.
    """
    if not destination.iata_code:
        fs = get_flight_search_service()
        destination.iata_code = fs.get_iata_code(destination.city_name)

    # Ensure IATA code was actually found
    if not destination.iata_code:
        raise ValueError(
            f"Could not resolve IATA code for city: {destination.city_name}"
        )

    db_destination = models.Destination(**destination.model_dump())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    print(f"INFO: Destination created with ID: {db_destination.id}")
    return db_destination


def get_active_destinations(db: Session):
    """
    Fetches all destinations that are currently marked as active from the database.
    """
    destinations = (
        db.query(models.Destination).filter(models.Destination.is_active == True).all()
    )
    print(f"INFO: Found {len(destinations)} active destinations.")
    return destinations


def list_destinations(db: Session):
    """
    Retrieves a list of all flight destinations stored in the database.
    """
    destinations = db.query(models.Destination).all()
    print(f"INFO: Found {len(destinations)} destinations.")
    return destinations


def delete_specific_destination(db: Session, destination_id: int):
    """
    Removes a specific flight destination from the database by its ID.
    """
    destination = (
        db.query(models.Destination)
        .filter(models.Destination.id == destination_id)
        .first()
    )
    if destination:
        db.delete(destination)
        db.commit()
        print(f"INFO: Destination {destination_id} deleted.")


def delete_all_destinations(db: Session):
    """
    Clears all stored flight destinations from the database.
    """
    deleted_count = db.query(models.Destination).delete()
    db.commit()
    print(f"INFO: Deleted {deleted_count} destinations.")
