import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Jogo, Usuario, Partida

async def init_db():
    mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "boardgames_db")
    client = AsyncIOMotorClient(mongo_url)

    await init_beanie(database=client[db_name], document_models=[Jogo, Usuario, Partida])