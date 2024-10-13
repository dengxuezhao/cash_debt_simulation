from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def home():
    return "Hello, this is a simple Python app"

@app.get("/data")
async def get_data():
    return JSONResponse(content={"message": "This is some JSON data"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
