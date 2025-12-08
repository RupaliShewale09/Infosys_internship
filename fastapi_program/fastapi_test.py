from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/about")
def about():
    return {"name": "Rupali Sunil Shewale",
            "Course": "B.E.",
            "Branch": "CSE"}