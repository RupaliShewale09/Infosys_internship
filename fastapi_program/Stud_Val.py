from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

students = []
current_id = 1

# Pydantic Model with Validation
class Student(BaseModel):
    name: str  # string type
    age: int = Field(..., ge=18, le=60)  # Age must be between 18–60
    email: EmailStr  # Valid email only

# Welcome message 
@app.get("/")
def Welcome():
    return {"Title": "Student Management with Validation"}

# Add Student
@app.post("/student")
def add_student(student: Student):
    global current_id

    new_student = {
        "id": current_id,
        "name": student.name,
        "age": student.age,
        "email": student.email
    }

    students.append(new_student)
    current_id += 1

    return {
        "message": "Student added successfully",
        "student": new_student
    }

# Get All Students
@app.get("/students")
def get_students():
    return students

# Get Student by ID
@app.get("/student/{student_id}")
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return {
                "status": "found",
                "student": s
            }

    return {
        "status": "not found",
        "message": "Student does not exist"
    }
