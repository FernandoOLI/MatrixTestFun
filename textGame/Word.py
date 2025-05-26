from textGame.Room import Room


class World:
    def __init__(self):
        self.rooms = {}
        self.build_world()

    def build_world(self):
        self.rooms['Sala 1'] = Room(
            "Sala 1",
            "Você está em uma sala branca com uma lâmpada que nunca apaga. Há uma porta ao norte.",
            {'norte': 'Sala 2'}
        )
        self.rooms['Sala 2'] = Room(
            "Sala 2",
            "Esta sala é idêntica à anterior... exceto por um espelho que não reflete nada.",
            {'sul': 'Sala 1', 'leste': 'Sala 3'},
            items=["espelho negro"]
        )
        self.rooms['Sala 3'] = Room(
            "Sala 3",
            "Paredes cobertas de símbolos que mudam quando você não está olhando.",
            {'oeste': 'Sala 2', 'norte': 'Sala Glitch'},
            log="Log 1: agente não percebe que as salas estão em loop."
        )
        self.rooms['Sala Glitch'] = Room(
            "Sala Glitch",
            "A parede... pi-s-c-a... *zzzzttt*... tudo se repete...",
            {'sul': 'Sala 3'},
            items=["painel quebrado"],
            log="Experimento 42: a simulação está instável.",
            glitch=True
        )
