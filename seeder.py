import asyncio
import random
from app.database import init_mongo
from app.models import Jogo, Usuario, Partida, Mecanica
from beanie import PydanticObjectId

async def seed():
    print("🌱 Iniciando o Seeder...")
    
    await init_mongo()

    print("🧹 Limpando dados antigos...")
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
                Mecanica(nome="Negociação", descricao="Troca de recursos entre jogadores"),
                Mecanica(nome="Rolagem de Dados", descricao="Define a produção de recursos")
            ]
        },
        {
            "titulo": "Ticket to Ride",
            "ano_lancamento": 2004,
            "categoria": "Família",
            "mecanicas": [
                Mecanica(nome="Coleção de Conjuntos", descricao="Juntar cartas da mesma cor"),
                Mecanica(nome="Construção de Rotas", descricao="Ligar cidades no mapa")
            ]
        },
        {
            "titulo": "Pandemic",
            "ano_lancamento": 2008,
            "categoria": "Cooperativo",
            "mecanicas": [
                Mecanica(nome="Pontos de Ação", descricao="4 ações por turno"),
                Mecanica(nome="Gestão de Mão", descricao="Cartas de cidade para cura")
            ]
        },
        {
            "titulo": "Wingspan",
            "ano_lancamento": 2019,
            "categoria": "Estratégia Leve",
            "mecanicas": [
                Mecanica(nome="Engine Building", descricao="Melhorar ações futuras"),
                Mecanica(nome="Seleção de Cartas", descricao="Pássaros com poderes")
            ]
        },
        {
            "titulo": "Terraforming Mars",
            "ano_lancamento": 2016,
            "categoria": "Estratégia Pesada",
            "mecanicas": [
                Mecanica(nome="Gestão de Recursos", descricao="Muitos cubos de recursos"),
                Mecanica(nome="Draft de Cartas", descricao="Escolher cartas no início")
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
        qtd_jogos = random.randint(1, 3)
        user.prateleira = random.sample(jogos_objs, qtd_jogos)
        
        await user.insert()
        users_objs.append(user)

    print(f"✅ {len(users_objs)} usuários criados com prateleiras preenchidas.")

    print("⚔️ Simulando Partidas...")
    
    locais = ["Casa da Alice", "Luderia Central", "Evento de Anime", "Online"]
    partidas_criadas = 0

    for _ in range(15):
        jogo_escolhido = random.choice(jogos_objs)
        jogadores_partida = random.sample(users_objs, k=random.randint(2, 4))
        vencedor = random.choice(jogadores_partida)
        
        partida = Partida(
            local=random.choice(locais),
            jogo=jogo_escolhido,       
            jogadores=jogadores_partida, 
            vencedor=vencedor           
        )
        await partida.insert()
        partidas_criadas += 1

    print(f"✅ {partidas_criadas} partidas registradas.")
    print("\n🚀 Seeder concluído com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed())