from fastapi import FastAPI, HTTPException
from app.routers.user_routes import user_router
from app.routers.devices_routes import devices_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API Tá funcionando"}

app.include_router(user_router)
app.include_router(devices_router)

