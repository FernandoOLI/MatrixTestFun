import requests
import pygame
from datetime import datetime
import os


class LLM_Controller:
    def __init__(self, model="mistral"):
        self.model = model
        self.OLLAMA_URL = "http://localhost:11434/api/generate"
        self._init_log_file()

    def _init_log_file(self):
        # Garante que o diretório existe
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", "llm_logs.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- Nova Sessão ({datetime.now()}) ---\n")

    def _log_action(self, prompt, response):
        log_path = os.path.join("logs", "llm_logs.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}]\nPrompt: {prompt}\nResposta: {response}\n\n")

    def get_action(self, game_state, user_input):
        context = "Você controla um agente verde. Responda APENAS com: esquerda, direita, cima ou baixo."
        prompt = f"{context}\nEstado: {game_state}\nInput: {user_input}"

        try:
            response = requests.post(
                self.OLLAMA_URL,
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=10
            )
            response.raise_for_status()
            action = response.json()['response'].strip().lower()
            self._log_action(prompt, action)
            return action
        except requests.exceptions.RequestException as e:
            error_msg = f"Erro na requisição: {str(e)}"
        except Exception as e:
            error_msg = f"Erro inesperado: {str(e)}"

        self._log_action(prompt, error_msg)
        return None