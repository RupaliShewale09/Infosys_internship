from fastapi import FastAPI, Request

app = FastAPI()

# GET METHOD
@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}

@app.get("/greet {username}")
def greet(username: str):
    return {"message": f"Hello {username}!"}

# POST METHOD
@app.post("/add")
async def add(request: Request):
    data = await request.json()   
    a = data.get("a")
    b = data.get("b")
    return {"result": a + b}
