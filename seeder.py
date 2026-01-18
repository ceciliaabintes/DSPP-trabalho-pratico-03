import asyncio
import random
import sys
import os

sys.path.insert(0, os.getcwd())

from app.database import init_mongo

from app.models import Jogo, Usuario, Partida, Mecanica, Avaliacao
from beanie import PydanticObjectId

async def seed():
    print("🌱 Iniciando o Seeder...")
    
    try:
        await init_mongo()
        print("✅ Conectado ao MongoDB.")
    except Exception as e:
        print(f"❌ Erro ao conectar no Mongo: {e}")
        return

    print("🧹 Limpando dados antigos...")
    await Avaliacao.delete_all() 
    await Partida.delete_all()
    await Usuario.delete_all()
    await Jogo.delete_all()

    print("🎲 Criando Jogos...")
    
    jogos_data = [
        {
            "titulo": "Catan",
            "ano_lancamento": 1995,
            "categoria": "Estratégia",
            "mecanicas": [
                Mecanica(nome="Negociação", descricao="Troca de recursos"),
                Mecanica(nome="Gestão de Mão", descricao="Cartas de desenvolvimento")
            ]
        },
        {
            "titulo": "Ticket to Ride",
            "ano_lancamento": 2004,
            "categoria": "Família",
            "mecanicas": [
                Mecanica(nome="Coleção de Conjuntos", descricao="Cartas de vagão"),
                Mecanica(nome="Construção de Rotas", descricao="Trens no mapa")
            ]
        },
        {
            "titulo": "Pandemic",
            "ano_lancamento": 2008,
            "categoria": "Cooperativo",
            "mecanicas": [
                Mecanica(nome="Pontos de Ação", descricao="4 ações por turno"),
                Mecanica(nome="Gestão de Mão", descricao="Limite de cartas")
            ]
        },
        {
            "titulo": "Azul",
            "ano_lancamento": 2017,
            "categoria": "Abstrato",
            "mecanicas": [
                Mecanica(nome="Draft Aberto", descricao="Pegar azulejos"),
                Mecanica(nome="Reconhecimento de Padrões", descricao="Montar parede")
            ]
        }
    ]

    jogos_objs = []
    for j_data in jogos_data:
  
        jogo = Jogo(**j_data)
        await jogo.insert()
        jogos_objs.append(jogo)
    
    print(f"✅ {len(jogos_objs)} jogos inseridos.")

    print("busts Criando Usuários...")
    
    users_data = [
        {"nome": "Alice Silva", "email": "alice@email.com"},
        {"nome": "Bruno Souza", "email": "bruno@email.com"},
        {"nome": "Carlos Mendes", "email": "carlos@email.com"},
        {"nome": "Diana Prince", "email": "diana@email.com"}
    ]

    users_objs = []
    for u_data in users_data:
        user = Usuario(**u_data)
 
        if jogos_objs:
            qtd_jogos = random.randint(1, 3)
            user.prateleira = random.sample(jogos_objs, qtd_jogos)
        
        await user.insert()
        users_objs.append(user)

    print(f"✅ {len(users_objs)} usuários criados.")

    print("⚔️ Simulando Partidas...")
    
    locais = ["Casa da Alice", "Luderia Central", "Evento de Anime", "Online"]
    
    if len(users_objs) >= 2:
        for _ in range(10):
            jogo_escolhido = random.choice(jogos_objs)
            jogadores_partida = random.sample(users_objs, k=random.randint(2, len(users_objs)))
            vencedor = random.choice(jogadores_partida)
            
            partida = Partida(
                local=random.choice(locais),
                jogo=jogo_escolhido,
                jogadores=jogadores_partida,
                vencedor=vencedor
            )
            await partida.insert()
        print("✅ 10 partidas registradas.")


    print("⭐ Gerando Avaliações...")
    for user in users_objs:
        jogos_avaliados = random.sample(jogos_objs, k=random.randint(1, 2))
        for jogo in jogos_avaliados:
            av = Avaliacao(
                usuario=user,
                jogo=jogo,
                nota=random.randint(3, 5), 
                comentario="Jogo muito bom!"
            )
            await av.insert()
    print("✅ Avaliações geradas.")

    print("\n🚀 Seeder concluído com sucesso!")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed())