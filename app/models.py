from datetime import datetime
from typing import Annotated 
from beanie import Document, Link, Indexed 
from pydantic import BaseModel, Field

class Mecanica(BaseModel):
    nome: str 
    descricao: str | None = None

class Jogo(Document):
    titulo: Annotated[str, Indexed(unique=True)]
    ano_lancamento: int
    categoria: str 
    mecanicas: list[Mecanica] = []

    class Settings:
        name = "jogos"

class Usuario(Document):
   nome: str 
   email: Annotated[str, Indexed(unique=True)]
   pratileira: list[Link[Jogo]] = []

   class Settings:
       name = "usuarios"

class Partida(Document):
    data: datetime = Field(default_factory=datetime.now)
    local: str | None = None
    jogo: Link[Jogo]
    jogadores: Link[Usuario] | None = None

    class Settings:
        name = "partidas"