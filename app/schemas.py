from pydantic import BaseModel 
from datetime import datetime 

class JogoCreate(BaseModel):
    titulo: str
    ano_lancamento: int
    categoria: str
    mecanicas: list[str] = []

class UsuarioCreate(BaseModel):
    nome: str
    email: str 

class PartidaCreate(BaseModel):
    jogo_id: str 
    jogadores_ids: list[str] = []
    local: str | None = None

class AddPrateleira(BaseModel):
    usario_id: str 
    jogo_id: str 

# schemas de saída
class JogoRead(BaseModel):
    id: str 
    titulo: str
    ano_lancamento: int
    categoria: str 

class UsuarioRead(BaseModel):
    id: str 
    nome: str 
    email: str
    pratileira: list[JogoRead] = []