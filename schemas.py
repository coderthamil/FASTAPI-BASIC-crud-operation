from pydantic import BaseModel
from uuid import UUID
# Schema for creating employee (request body)
class EmployeeCreate(BaseModel):
    name: str
    age: int
    email: str

# Schema for returning employee (response body)
class EmployeeSchema(BaseModel):
    id: UUID
    name: str
    age: int
    email: str

    class Config:
        orm_mode = True


'''Key Points
BaseModel → the base class for defining Pydantic schemas.

orm_mode = True → lets FastAPI convert SQLAlchemy ORM objects into Pydantic models automatically.

This schema is separate from your SQLAlchemy Employee model (which inherits from Base in database.py).class config: orm_mode = true is to convert the objects to orm model'''


'''⚡ How it fits together
SQLAlchemy model (Employee) → defines the table and columns in the database.

Pydantic schema (EmployeeSchema) → defines how data is validated and returned in API responses.

In routes, you use Depends(get_db) to query with SQLAlchemy, then return results serialized through Pydantic.'''