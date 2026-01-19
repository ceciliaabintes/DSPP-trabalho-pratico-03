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
    vencedor_id: str | None = None

class AddPrateleira(BaseModel):
    usuario_id: str 
    jogo_id: str 

class JogoRead(BaseModel):
    id: str 
    titulo: str
    ano_lancamento: int
    categoria: str 

class UsuarioRead(BaseModel):
    id: str 
    nome: str 
    email: str
    prateleira: list[JogoRead] = []

class JogoUpdate(BaseModel):
    titulo: str | None = None
    ano_lancamento: int | None = None
    categoria: str | None = None
    mecanicas: list[str] | None = None

class AvaliacaoCreate(BaseModel):
    usuario_id: str
    jogo_id: str
    nota: int 
    comentario: str | None = None