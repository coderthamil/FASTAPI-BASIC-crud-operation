from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal, get_db
from models import Employee
from schemas import  *
from fastapi import HTTPException
from uuid import UUID
from sqlalchemy.exc import IntegrityError
app = FastAPI()


# Create all tables defined in models
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "hello fastapi"}
'''so my post route url is employees of my data is to be is dictionary format  also the object name is employee so i need in format of specified schema, '''
'''🔎 Why db: Session = Depends(get_db) is needed
Depends(get_db) → tells FastAPI: “Before running this route, call get_db() and give me a database session.”

db: Session → is the type hint showing that db will be a SQLAlchemy session object.

Together, this means every request to /employees/ gets:

A fresh database session (SessionLocal()).

That session is automatically closed after the request (because of the finally: db.close() in get_db()).

So you don’t manually open/close sessions in your route — FastAPI handles it via dependency injection.'''
"""Employee → is your SQLAlchemy model (the table definition).

new_employee → is a new Python object instance of that model.

The parameters (name, age, email) are the fields you defined in the model.

The values (employee.name, employee.age, employee.email) come from the validated Pydantic schema that FastAPI parsed from the request body.

So new_employee is literally the new record object you’re preparing to insert into the database."""
@app.post("/employees", response_model=EmployeeSchema)
async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    # 🔎 Step 1: Check if email already exists in the database
    # This avoids duplicate entries and prevents hitting the unique constraint error
    existing = db.query(Employee).filter(Employee.email == employee.email).first()
    if existing:
        # If an employee with the same email is found, return a clean error response
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔎 Step 2: Create a new Employee object
    # Using **employee.dict() automatically maps name, age, email from the request body
    new_employee = Employee(**employee.dict())

    # 🔎 Step 3: Stage the new record (not yet written to DB)
    db.add(new_employee)

    # 🔎 Step 4: Commit the transaction (write permanently to DB)
    db.commit()

    # 🔎 Step 5: Refresh the object so it has the generated UUID and any defaults
    db.refresh(new_employee)

    # 🔎 Step 6: Return the new employee object
    # FastAPI will serialize it into JSON using EmployeeSchema
    return new_employee


# @app.post("/employees", response_model=EmployeeSchema)
# async def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
#     # Create a new Employee object from the validated request body
#     new_employee = Employee(
#         name=employee.name,
#         age=employee.age,
#         email=employee.email
#     )

#     # Stage the new record (not yet written to DB)
#     db.add(new_employee)

#     try:
#         # Attempt to commit the transaction (write permanently)
#         db.commit()

#         # Refresh the object so it has the generated UUID and any defaults
#         db.refresh(new_employee)

#     except IntegrityError:
#         # If commit fails due to duplicate email (unique constraint violation),
#         # rollback the transaction to keep the session clean
#         db.rollback()

#         # Return a proper HTTP error response instead of crashing
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Return the new employee object, FastAPI will serialize it using EmployeeSchema
#     return new_employee

@app.get("/employees/{id}",response_model=EmployeeSchema)
async def get_employee(id:str,db:Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id==id).first()
    if employee is None:
        return {"message":"Employee not found"}
    return employee
   
'''db.query(Employee) → starts a query on the Employee table.

.filter(Employee.id == id) → applies a filter condition.

.first() → fetches the first matching record (or None if not found).

if employee is None: → checks if no record exists.

return employee → returns the ORM object, which FastAPI converts into JSON using EmployeeSchema because of orm_mode.'''

@app.put("update/{id}",response_model=EmployeeSchema)
async def update_employee(id:UUID,employee:EmployeeCreate,db:Session = Depends(get_db)):
    existing = db.query(Employee).filter(Employee.id == id).first()
    if existing is None:
        raise HTTPException(status_code=404,detail ="Employee not Found")

    existing.name = employee.name
    existing.age = employee.age
    existing.email = employee.email

    db.commit()
    db.refresh(existing)
    return existing


@app.delete("/employees/{id}")
async def delete_employee(id: UUID, db: Session = Depends(get_db)):
    existing = db.query(Employee).filter(Employee.id == id).first()
    if existing is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(existing)
    db.commit()
    return {"detail": "Employee deleted successfully"}