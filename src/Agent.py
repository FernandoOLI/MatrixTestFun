import requests


class Agent:
    def __init__(self, world):
        self.current_room = 'Sala 1'
        self.world = world
        self.history = []
        self.inventory = []

    def get_current_description(self):
        room = self.world.rooms[self.current_room]
        desc = room.description
        if room.glitch:
            desc += "\n⚠️ Algo está errado aqui. Há distorções visuais."
        if room.items:
            desc += f"\nVocê vê aqui: {', '.join(room.items)}"
        return f"{desc}\nSaídas: {', '.join(room.exits.keys())}"

    def move(self, direction):
        room = self.world.rooms[self.current_room]
        if direction in room.exits:
            self.current_room = room.exits[direction]
            return f"Você se move para o {direction}."
        else:
            return "Não há saída nessa direção."

    def interagir(self, acao):
        acao = acao.lower()
        room = self.world.rooms[self.current_room]

        if acao.startswith("investigar"):
            item = acao.replace("investigar", "").strip()
            if item in room.items:
                return f"Você investiga o {item}. Há algo estranho nele..."
            else:
                return f"Você não encontra nada relevante com '{item}'."

        elif acao.startswith("pegar"):
            item = acao.replace("pegar", "").strip()
            if item in room.items:
                self.inventory.append(item)
                room.items.remove(item)
                return f"Você pegou o item: {item}"
            else:
                return "Esse item não está aqui."

        elif acao.startswith("ler log"):
            if room.log:
                return f"📄 Log secreto encontrado:\n{room.log}"
            else:
                return "Não há nenhum log nesta sala."

        elif any(direcao in acao for direcao in ['norte', 'sul', 'leste', 'oeste']):

            for direcao in ['norte', 'sul', 'leste', 'oeste']:

                if direcao in acao:
                    return self.move(direcao)

        else:
            return f"O agente tenta: '{acao}' (ação não reconhecida como válida)."

    def think(self, description):
        prompt = f"""
Você é um agente em um mundo simulado. Aqui está a descrição atual do ambiente:

\"\"\"{description}\"\"\"

Aja com base no que percebe. Escolha uma ação entre: mover-se (norte, sul...), investigar algo, pegar um item ou ler um log. Retorne apenas a ação.
"""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        result = response.json()["response"].strip().lower()
        self.history.append((description, result))
        return result
