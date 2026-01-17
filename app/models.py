from datetime import datetime
from typing import Annotated, List, Optional
from beanie import Document, Link, Indexed
from pydantic import BaseModel, Field

class Mecanica(BaseModel):
    nome: str
    descricao: str | None = None

class Jogo(Document):
    """
    Coleção de Jogos.
    Indexed() permite busca textual rápida.
    """
    titulo: Annotated[str, Indexed()] 
    ano_lancamento: int
    categoria: str
    mecanicas: List[Mecanica] = []  
    
    class Settings:
        name = "jogos"

class Usuario(Document):
    """
    Coleção de Usuários.
    """
    nome: str
    email: Annotated[str, Indexed(unique=True)]
    
   
    prateleira: List[Link[Jogo]] = [] 
    
    class Settings:
        name = "usuarios"

class Partida(Document):
    """
    Coleção de Partidas (Logs).
    """
    data: datetime = Field(default_factory=datetime.now)
    local: str | None = None
    
    jogo: Link[Jogo]
    jogadores: List[Link[Usuario]]
    vencedor: Optional[Link[Usuario]] = None
    
    class Settings:
        name = "partidas"