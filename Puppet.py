import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QAction, QFileDialog, QDialog, QVBoxLayout, QRadioButton, QPushButton
from PyQt5.QtCore import Qt
import os
import subprocess
import threading
import pygame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Puppet")
        self.setGeometry(100, 100, 640, 640)  # Define o tamanho da janela

        # Menu
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archives")

        # Ações do menu
        add_games_action = QAction("Add Games", self)
        add_games_action.triggered.connect(self.add_games)
        file_menu.addAction(add_games_action)

        open_games_action = QAction("Open Games", self)
        open_games_action.triggered.connect(self.open_games)
        file_menu.addAction(open_games_action)

        # Botão de configurações
        config_action = QAction("Configurations", self)
        config_action.triggered.connect(self.open_configurations)
        menubar.addAction(config_action)

    def add_games(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            destination = os.path.join("games", os.path.basename(folder_path))
            if not os.path.exists(destination):
                os.makedirs(destination)
            for item in os.listdir(folder_path):
                s = os.path.join(folder_path, item)
                d = os.path.join(destination, item)
                if os.path.isdir(s):
                    os.makedirs(d)
                else:
                    with open(s, 'rb') as fsrc, open(d, 'wb') as fdst:
                        fdst.write(fsrc.read())

    def open_games(self):
        folder_path = "games"  # Define o diretório padrão
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_filter = "Executable Files (*.exe)"
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Game File", folder_path, file_filter, options=options
        )
        if file_path:
            self.launch_game(file_path)

    def launch_game(self, game_path):
        try:
            self.run_game_in_pygame(game_path)
        except Exception as e:
            print(f"Erro ao iniciar o jogo: {e}")

    def run_game_in_pygame(self, game_path):
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

    def open_configurations(self):
        config_dialog = ConfigurationsDialog(self)
        config_dialog.exec_()

class ConfigurationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Configurations")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.rb_816x624 = QRadioButton("816x624")
        self.rb_816x624.setChecked(True)
        self.rb_816x624.toggled.connect(self.on_resolution_change)
        layout.addWidget(self.rb_816x624)

        self.rb_1280x720 = QRadioButton("1280x720")
        self.rb_1280x720.toggled.connect(self.on_resolution_change)
        layout.addWidget(self.rb_1280x720)

        self.rb_1280x800 = QRadioButton("1280x800")
        self.rb_1280x800.toggled.connect(self.on_resolution_change)
        layout.addWidget(self.rb_1280x800)

        self.rb_1280x920 = QRadioButton("1280x920")
        self.rb_1280x920.toggled.connect(self.on_resolution_change)
        layout.addWidget(self.rb_1280x920)

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save_config)
        layout.addWidget(btn_save)

        self.setLayout(layout)

    def on_resolution_change(self):
        if self.rb_816x624.isChecked():
            self.selected_resolution = (816, 624)
        elif self.rb_1280x720.isChecked():
            self.selected_resolution = (1280, 720)
        elif self.rb_1280x800.isChecked():
            self.selected_resolution = (1280, 800)
        elif self.rb_1280x920.isChecked():
            self.selected_resolution = (1280, 920)

    def save_config(self):
        # Salva a resolução selecionada em um arquivo de configuração
        with open("config.txt", "w") as f:
            f.write(f"resolution={self.selected_resolution[0]}x{self.selected_resolution[1]}")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
