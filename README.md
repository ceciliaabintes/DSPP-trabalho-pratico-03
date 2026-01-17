classDiagram
    class Jogo {
        ObjectId id
        String titulo
        Int ano_lancamento
        Mecanica[] mecanicas
    }
    class Usuario {
        ObjectId id
        String nome
        Link~Jogo~[] prateleira
    }
    class Partida {
        ObjectId id
        Link~Jogo~ jogo
        Link~Usuario~[] jogadores
    }
    Usuario "1" --> "*" Jogo : possui
    Partida "*" --> "1" Jogo : refere-se
    Partida "*" --> "*" Usuario : jogado por