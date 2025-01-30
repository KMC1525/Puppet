import os
import subprocess
import threading
import pygame
from cefpython3 import cefpython as cef
from py_mini_racer import py_mini_racer
import sys

def run_rpgm_game(game_path):
    def game_thread():
        # Inicia o jogo RPG Maker
        game_process = subprocess.Popen([game_path])
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_process.terminate()
                    game_process.wait()
            screen.fill((0, 0, 0))
            pygame.display.flip()
        pygame.quit()

    # Configura a janela do Pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    pygame.display.set_caption("RPG Maker Game")
    
    # Executa o jogo em uma thread separada
    thread = threading.Thread(target=game_thread)
    thread.start()

def run_cef_game(game_path):
    def cef_thread():
        sys.excepthook = cef.ExceptHook
        cef.Initialize()
        browser = cef.CreateBrowserSync(url=game_path, window_title="RPG Maker Game")
        cef.MessageLoop()
        cef.Shutdown()

    thread = threading.Thread(target=cef_thread)
    thread.start()

def run_js_game(js_code):
    ctx = py_mini_racer.MiniRacer()
    ctx.eval(js_code)

if __name__ == "__main__":
    game_path = "games/Game.exe"
    run_rpgm_game(game_path)
