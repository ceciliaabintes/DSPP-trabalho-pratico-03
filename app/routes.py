from fastapi import APIRouter, HTTPException
from app.models import Jogo, Usuario, Partida, Mecanica, Avaliacao
from app.schemas import (
    JogoCreate, UsuarioCreate, PartidaCreate, 
    AddPrateleira, UsuarioRead, JogoRead, AvaliacaoCreate, JogoUpdate
)
from beanie import PydanticObjectId
from beanie.operators import RegEx, GTE, In

router = APIRouter()

@router.post("/jogos/", tags=["Jogos"])
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

@router.get("/jogos/", tags=["Jogos"])
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

@router.put("/jogos/{id}", tags=["Jogos"])
async def atualizar_jogo(id: str, dados: JogoUpdate):
    jogo = await Jogo.get(PydanticObjectId(id))
    if not jogo:
        raise HTTPException(404, "Jogo não encontrado")
    
    update_data = dados.model_dump(exclude_unset=True)

    if "mecanicas" in update_data:
        update_data["mecanicas"] = [
            Mecanica(nome=m) for m in update_data["mecanicas"]
        ]

    await jogo.update({"$set": update_data})
    return {"msg": "Jogo atualizado com sucesso", "dados": update_data}

@router.delete("/jogos/{id}", tags=["Jogos"])
async def deletar_jogo(id: str):
    jogo = await Jogo.get(PydanticObjectId(id))
    if not jogo:
        raise HTTPException(404, "Jogo não encontrado")
    
    await jogo.delete()
    return {"msg": "Jogo deletado com sucesso"}

@router.post("/usuarios/", response_model=UsuarioRead, tags=["Usuários"])
async def criar_usuario(dados: UsuarioCreate):
    novo_user = Usuario(**dados.model_dump())
    await novo_user.insert()
    return UsuarioRead(
        id=str(novo_user.id), 
        nome=novo_user.nome, 
        email=novo_user.email,
        prateleira=[]
    )

@router.post("/usuarios/prateleira", tags=["Usuários"])
async def add_prateleira(dados: AddPrateleira):
    user = await Usuario.get(PydanticObjectId(dados.usuario_id))
    jogo = await Jogo.get(PydanticObjectId(dados.jogo_id))
    
    if not user or not jogo:
        raise HTTPException(404, "Usuário ou Jogo não encontrado")
    
    user.prateleira.append(jogo)
    await user.save()
    return {"msg": "Jogo adicionado à prateleira"}

@router.get("/usuarios/{id}", response_model=UsuarioRead,tags=["Usuários"])
async def obter_usuario(id: str):
    try:
        user_id = PydanticObjectId(id)
    except:
        raise HTTPException(400, "ID inválido")

    user = await Usuario.get(user_id)
    
    if not user:
        raise HTTPException(404, "Usuário não encontrado")
    
    ids_jogos = [link.ref.id for link in user.prateleira]
    
    jogos_completos = await Jogo.find(In(Jogo.id, ids_jogos)).to_list()

    lista_jogos_read = [
        JogoRead(
            id=str(j.id),
            titulo=j.titulo,
            ano_lancamento=j.ano_lancamento,
            categoria=j.categoria
        )
        for j in jogos_completos
    ]
    
    return UsuarioRead(
        id=str(user.id),
        nome=user.nome,
        email=user.email,
        prateleira=lista_jogos_read
    )

@router.get("/usuarios/", response_model=list[UsuarioRead], tags=["Usuários"])
async def listar_usuarios():
    users = await Usuario.find_all().to_list()
    resultado = []
    for u in users:
        resultado.append(
            UsuarioRead(id=str(u.id), nome=u.nome, email=u.email, prateleira=[])
        )
    return resultado

@router.post("/partidas/", tags=["Partidas"])
async def registrar_partida(dados: PartidaCreate):
    jogo = await Jogo.get(PydanticObjectId(dados.jogo_id))
    if not jogo: raise HTTPException(404, "Jogo inexistente")
    
    lista_ids = [PydanticObjectId(uid) for uid in dados.jogadores_ids]
    jogadores_objs = await Usuario.find(In(Usuario.id, lista_ids)).to_list()
    
    if len(jogadores_objs) != len(lista_ids):
        raise HTTPException(404, "Alguns jogadores não foram encontrados")

    vencedor_obj = None
    if dados.vencedor_id:
        vencedor_obj = await Usuario.get(PydanticObjectId(dados.vencedor_id))

    partida = Partida(
        jogo=jogo,
        jogadores=jogadores_objs,
        vencedor=vencedor_obj,
        local=dados.local
    )
    
    await partida.insert()
    return {"msg": "Partida registrada!", "id": str(partida.id)}

@router.post("/avaliacoes/", tags=["Avaliações"])
async def avaliar_jogo(dados: AvaliacaoCreate):
    usuario = await Usuario.get(PydanticObjectId(dados.usuario_id))
    jogo = await Jogo.get(PydanticObjectId(dados.jogo_id))
    
    if not usuario or not jogo:
        raise HTTPException(404, "Usuário ou Jogo não encontrado")
    
    nova_avaliacao = Avaliacao(
        usuario=usuario,
        jogo=jogo,
        nota=dados.nota,
        comentario=dados.comentario
    )
    
    await nova_avaliacao.insert()
    return {"msg": f"O jogo {jogo.titulo} recebeu nota {dados.nota}!"}

@router.get("/relatorios/avaliacoes-jogo/{jogo_id}", tags=["Relatórios"])
async def relatorio_avaliacoes_jogo(jogo_id: str):

    pipeline = [
        {"$group": {
            "_id": "$jogo.$id",
            "media_notas": {"$avg": "$nota"},
            "total_avaliacoes": {"$sum": 1}
        }
        },
        {"$lookup": {
            "from": "jogos",
            "localField": "_id",
            "foreignField": "_id",
            "as": "detalhes_jogo"
        }},
        {"$project": {
            "_id": 0,
            "jogo": {"$arrayElemAt": ["$detalhes_jogo.titulo", 0]},
            "media": {"$round": ["$media_notas", 1]}, 
            "qtd_votos": "$total_avaliacoes"
        }},
        {"$sort": {"media": -1}}
    ]

    col = Avaliacao.get_pymongo_collection()
    resultado = await col.aggregate(pipeline).to_list(length=None)
    return resultado

@router.get("/relatorios/jogos-populares", tags=["Relatórios"])
async def relatorio_agregacao():
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
            "_id": 0,
            "titulo_jogo": {"$arrayElemAt": ["$detalhes_jogo.titulo", 0]},
            "total_partidas": "$total"
        }}
    ]
    
    col = Partida.get_pymongo_collection()
    resultado = await col.aggregate(pipeline).to_list(length=None)
    return resultado