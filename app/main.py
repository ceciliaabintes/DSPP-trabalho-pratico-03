from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_mongo
from app.routes import router as app_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    yield

app =  FastAPI(
    title="API para Avaliação de Jogos de Tabuleiro",
    description="API desenvolvida para gerenciar avaliações de jogos de tabuleiro.",
    version="3.0.0",
    lifespan=lifespan
)

app.include_router(app_router)