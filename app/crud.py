from sqlalchemy.orm import Session

from app import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    print(f"📝 [CRUD] Creating user: {user.first_name} {user.last_name} ({user.email})")
    # Using ** unpacks the Pydantic dictionary directly into the SQLAlchemy model!
    db_user = models.User(**user.model_dump())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"✅ [CRUD] User created successfully with ID: {db_user.id}")

    return db_user


def get_user_by_email(db: Session, email: str):
    print(f"🔍 [CRUD] Searching for user with email: {email}")
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        print(
            f"✅ [CRUD] User found: ID={user.id}, Name={user.first_name} {user.last_name}"
        )
    else:
        print(f"❌ [CRUD] User not found with email: {email}")
    return user


def create_destination(db: Session, destination: schemas.DestinationCreate):
    print(
        f"📝 [CRUD] Creating destination: {destination.city_name} ({destination.iata_code}) - Target: ₹{destination.target_price}"
    )
    db_destination = models.Destination(**destination.model_dump())

    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    print(f"✅ [CRUD] Destination created successfully with ID: {db_destination.id}")

    return db_destination


def get_active_destinations(db: Session):
    print("🔍 [CRUD] Fetching all active destinations...")
    destinations = (
        db.query(models.Destination).filter(models.Destination.is_active == True).all()
    )
    print(f"✅ [CRUD] Found {len(destinations)} active destination(s)")
    return destinations


def list_destinations(db: Session):
    print("🔍 [CRUD] Listing all destinations...")
    destinations = db.query(models.Destination).all()
    print(f"✅ [CRUD] Found {len(destinations)} destination(s)")
    for dest in destinations:
        print(
            f"   - ID: {dest.id}, City: {dest.city_name}, IATA: {dest.iata_code}, Target Price: ₹{dest.target_price}, Active: {dest.is_active}"
        )
    return destinations


def delete_specific_destination(db: Session, destination_id: int):
    print(f"🗑️ [CRUD] Deleting destination with ID: {destination_id}")
    destination = (
        db.query(models.Destination)
        .filter(models.Destination.id == destination_id)
        .first()
    )
    if destination:
        db.delete(destination)
        db.commit()
        print(f"✅ [CRUD] Destination with ID {destination_id} deleted successfully.")
    else:
        print(
            f"❌ [CRUD] Destination with ID {destination_id} not found. No deletion performed."
        )


def delete_all_destinations(db: Session):
    print("🗑️ [CRUD] Deleting all destinations...")
    deleted_count = db.query(models.Destination).delete()
    db.commit()
    print(f"✅ [CRUD] Deleted {deleted_count} destination(s) successfully.")
