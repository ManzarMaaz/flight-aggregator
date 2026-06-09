from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

print("\n💾 [DATABASE] Creating SQLAlchemy engine...")
# Creating the SQLAlchemy engine
engine = create_engine(settings.DATABASE_URL, echo=False)
print("✅ [DATABASE] SQLAlchemy engine created successfully.")

print("\n💾 [DATABASE] Setting up SessionLocal factory...")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("✅ [DATABASE] SessionLocal factory initialized.\n")

Base = declarative_base()

def get_db():
    print("[DATABASE] Creating new database session...")
    db = SessionLocal()
    try:
        yield db
    finally:
        print("[DATABASE] Closing database session...")
        db.close()
