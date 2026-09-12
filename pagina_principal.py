import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from login import TelaLogin


# Caminho da pasta do projeto
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


class TelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # Caminho da tela principal
        caminho = os.path.join(
            BASE_DIR,
            "tela",
            "principal.ui"
        )

        print("Carregando principal.ui...")

        # Carrega a tela principal
        uic.loadUi(
            caminho,
            self
        )

        print("principal.ui carregada!")


class Sistema:

    def __init__(self):

        # Cria a aplicação
        self.app = QApplication(sys.argv)

        # Cria o LOGIN DEFINITIVO
        self.login = TelaLogin()

        # A tela principal ainda não foi criada
        self.principal = None

        # Quando o login for realizado com sucesso,
        # chama a função abrir_principal
        self.login.login_sucesso.connect(
            self.abrir_principal
        )

    def abrir_principal(self):

        print("Abrindo tela principal...")

        # Fecha a tela de login
        self.login.close()

        # Cria a tela principal
        self.principal = TelaPrincipal()

        # Mostra a tela principal
        self.principal.show()

        # Coloca a janela em primeiro plano
        self.principal.raise_()
        self.principal.activateWindow()

    def executar(self):

        # Mostra o login
        self.login.show()

        # Executa o programa
        sys.exit(
            self.app.exec_()
        )


if __name__ == "__main__":

    sistema = Sistema()

    sistema.executar()