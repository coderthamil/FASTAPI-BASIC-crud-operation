# database.py

from sqlalchemy import create_engine
# create_engine → connects SQLAlchemy to your database

from sqlalchemy.orm import sessionmaker, declarative_base
# sessionmaker → creates session objects for DB transactions
# declarative_base → base class for ORM models

# PostgreSQL connection string
DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/FastAPI_Tutorial"

# Engine (actual DB connection)
engine = create_engine(DATABASE_URL)

# Session factory (used in get_db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
'''using declarative base you can define models'''
# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
