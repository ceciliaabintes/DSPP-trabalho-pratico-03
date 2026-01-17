from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_mongo
from app.routes import router as app_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    yield

app =  FastAPI(
    title="Api para Avaliação de Board Games",
    description="API desenvolvida para o trabalho prático 03 da disciplina DSPP",
    version="3.0.0",
    lifespan=lifespan
)

app.include_router(app_router)