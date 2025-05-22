import time

from src.Agent import Agent
from src.Word import World
class Simulate:
    def exibir_mapa_ascii(posicao_atual):
        mapa = {
            'Sala 1': (1, 1),
            'Sala 2': (0, 1),
            'Sala 3': (0, 2),
            'Sala Glitch': (-1, 2)
        }

        grid = [['   ' for _ in range(4)] for _ in range(4)]
        for sala, (x, y) in mapa.items():
            label = "AG" if sala == posicao_atual else sala[-1]
            grid[2 - x][y] = f"[{label}]"

        print("\nMapa ASCII:")
        for linha in grid:
            print(" ".join(linha))
        print()


    def start(self):
        world = World()
        agent = Agent(world)

        print("🧪 Simulação iniciada. A LLM (via Mistral/Ollama) está interagindo com o mundo...\n")

        for turno in range(10):
            time.sleep(1)
            desc = agent.get_current_description()
            Simulate.exibir_mapa_ascii(agent.current_room)

            print(f"\n📍 Sala atual: {agent.current_room}")
            print(f"📝 Descrição:\n{desc}")
            print(f"🎒 Inventário: {', '.join(agent.inventory) if agent.inventory else 'vazio'}\n")

            action = agent.think(desc)
            print(f"🤖 Ação sugerida pela LLM: {action}")

            resultado = agent.interagir(action)
            print(f"📌 Resultado: {resultado}")
            print("-" * 50)
            time.sleep(1)
