import os
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import Jogo, Usuario, Partida, Avaliacao

async def init_mongo():
    mongo_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    db_name = os.getenv("DB_NAME", "boardgames_tp3")
    
    try:
        client = AsyncIOMotorClient(mongo_url)
        await init_beanie(
            database=client[db_name],
            document_models=[Jogo, Usuario, Partida, Avaliacao]
        )
        print(f"🔌 Beanie inicializado no banco: {db_name}")
    except Exception as e:
        print(f"❌ Erro na conexão com Mongo: {e}")
        raise e