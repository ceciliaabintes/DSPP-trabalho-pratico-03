from fastapi import APIRouter, HTTPException, Query
from app.models import Jogo, Usuario, Partida, Mecanica
from app.schemas import (
    JogoCreate, UsuarioCreate, PartidaCreate, 
    AddPrateleira, UsuarioRead
)
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE # Operadores do Mongo

router = APIRouter()


@router.post("/jogos/")
async def criar_jogo(dados: JogoCreate):
    mecs = [Mecanica(nome=m) for m in dados.mecanicas]
    novo_jogo = Jogo(
        titulo=dados.titulo,
        ano_lancamento=dados.ano_lancamento,
        categoria=dados.categoria,
        mecanicas=mecs
    )
    await novo_jogo.insert()
    return novo_jogo

@router.get("/jogos/")
async def listar_jogos(
    ano_minimo: int | None = None, 
    busca_titulo: str | None = None 
):
    query = Jogo.find_all()
    
    if ano_minimo:
        query = query.find(GTE(Jogo.ano_lancamento, ano_minimo))
        
    if busca_titulo:
        query = query.find(RegEx(Jogo.titulo, busca_titulo, "i"))
        
    return await query.sort(-Jogo.ano_lancamento).to_list()

@router.post("/usuarios/", response_model=UsuarioRead)
async def criar_usuario(dados: UsuarioCreate):
    novo_user = Usuario(**dados.model_dump())
    await novo_user.insert()
    return UsuarioRead(
        id=str(novo_user.id), 
        nome=novo_user.nome, 
        email=novo_user.email
    )

@router.post("/usuarios/prateleira")
async def add_prateleira(dados: AddPrateleira):
    user = await Usuario.get(PydanticObjectId(dados.usuario_id))
    jogo = await Jogo.get(PydanticObjectId(dados.jogo_id))
    
    if not user or not jogo:
        raise HTTPException(404, "Usuário ou Jogo não encontrado")
    
    user.prateleira.append(jogo)
    await user.save()
    return {"msg": "Jogo adicionado à prateleira"}

@router.get("/usuarios/{id}", response_model=UsuarioRead)
async def obter_usuario(id: str):
    user = await Usuario.find_one(Usuario.id == PydanticObjectId(id), fetch_links=True)
    
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    
    return user

@router.post("/partidas/")
async def registrar_partida(dados: PartidaCreate):
    jogo = await Jogo.get(PydanticObjectId(dados.jogo_id))
    if not jogo: raise HTTPException(404, "Jogo inexistente")
    
    partida = Partida(
        jogo=jogo,
        jogadores=[PydanticObjectId(uid) for uid in dados.jogadores_ids],
        local=dados.local
    )
    if dados.vencedor_id:
        partida.vencedor = PydanticObjectId(dados.vencedor_id)
        
    await partida.insert()
    return {"msg": "Partida registrada!"}

@router.get("/relatorios/jogos-populares")
async def relatorio_agregacao():
    """
    Retorna a contagem de partidas por jogo.
    Requisito (e): Agregações com Pipeline
    """
    pipeline = [
        {"$group": {"_id": "$jogo.$id", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$lookup": {
            "from": "jogos",
            "localField": "_id",
            "foreignField": "_id",
            "as": "detalhes_jogo"
        }},
        {"$project": {
            "titulo_jogo": {"$arrayElemAt": ["$detalhes_jogo.titulo", 0]},
            "total_partidas": "$total"
        }}
    ]
    
    resultado = await Partida.aggregate(pipeline).to_list()
    return resultado