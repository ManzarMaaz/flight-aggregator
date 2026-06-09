from sqlalchemy import Boolean, Float, Column, Integer, String
from app.database import Base


class Destination(Base):

    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, index=True, nullable=False)
    iata_code = Column(String, index=True, nullable=False)
    target_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)