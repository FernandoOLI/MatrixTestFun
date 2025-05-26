import pygame
from simulateGame.LLM_Controller import LLM_Controller


class Simulate:
    def __init__(self, width=600, height=400):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Simulação LLM")
        self.clock = pygame.time.Clock()
        self.running = True
        self.llm = LLM_Controller()

        # Configurações do agente
        self.agent_speed = 5
        self.room_rect = pygame.Rect(50, 50, width - 100, height - 100)
        self.agent_rect = pygame.Rect(width // 2, height // 2, 20, 20)

        # Configurações de texto
        self.font = pygame.font.SysFont("Arial", 20)
        self.llm_feedback = "Pressione L para consultar o LLM"
        self.last_update_time = 0

    def start(self):
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self._ask_llm_for_action()

    def _ask_llm_for_action(self):
        game_state = f"Agente em {self.agent_rect.topleft}"
        user_input = "Mova-se!"

        action = self.llm.get_action(game_state, user_input)
        if action:
            self.llm_feedback = f"LLM disse: {action}"
            self._simulate_key_press(action)
        else:
            self.llm_feedback = "LLM não respondeu"

    def _simulate_key_press(self, action):
        key_mapping = {
            "esquerda": pygame.K_LEFT,
            "direita": pygame.K_RIGHT,
            "cima": pygame.K_UP,
            "baixo": pygame.K_DOWN
        }
        if action in key_mapping:
            pygame.event.post(pygame.event.Event(
                pygame.KEYDOWN, {"key": key_mapping[action]}
            ))

    def _update(self):
        keys = pygame.key.get_pressed()
        new_rect = self.agent_rect.copy()

        if keys[pygame.K_LEFT]: new_rect.x -= self.agent_speed
        if keys[pygame.K_RIGHT]: new_rect.x += self.agent_speed
        if keys[pygame.K_UP]: new_rect.y -= self.agent_speed
        if keys[pygame.K_DOWN]: new_rect.y += self.agent_speed

        if self.room_rect.contains(new_rect):
            self.agent_rect = new_rect

    def _render(self):
        self.screen.fill((0, 0, 0))

        # Desenha sala e agente
        pygame.draw.rect(self.screen, (70, 70, 70), self.room_rect)
        pygame.draw.rect(self.screen, (0, 255, 0), self.agent_rect)

        # Renderiza feedback do LLM
        text = self.font.render(self.llm_feedback, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()