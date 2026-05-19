import uuid
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from database import Base  # import Base from your database.py

class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)

"""Key Points
UUID(as_uuid=True) → PostgreSQL-native UUID type.

default=uuid.uuid4 → auto-generates a new UUID when inserting.

primary_key=True → makes it the primary key.

Base → comes from your database.py (Base = declarative_base())."""