from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("\n🚀 [ENDPOINT] POST /api/v1/users/ - User registration started")
    print(f"   Email: {user.email}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        print("❌ [ENDPOINT] Registration failed: Email already exists\n")
        raise HTTPException(status_code=400, detail="Email already registered")
    result = crud.create_user(db=db, user=user)
    print("✅ [ENDPOINT] User registration completed successfully\n")
    return result
