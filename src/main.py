from fastapi import FastAPI
from routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    MONGODB_URL = settings.MONGODB_URL
    MONGODB_DATABASE = settings.MONGODB_DATABASE
    app.mongo_conn = AsyncIOMotorClient(MONGODB_URL)
    app.db_client =  app.mongo_conn[MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()



app.include_router(data.router_data)