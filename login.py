import os

from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap


# Caminho da pasta do projeto
BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


class TelaLogin(QtWidgets.QMainWindow):

    # Sinal enviado quando o login estiver correto
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        # Caminho da tela de login definitiva
        caminho = os.path.join(
            BASE_DIR,
            "tela",
            "login.ui"
        )

        print("Carregando login.ui...")

        # Carrega a tela criada no Qt Designer
        uic.loadUi(
            caminho,
            self
        )

        print("login.ui carregada!")

        # Conecta o botão de entrar
        self.btn_entrar.clicked.connect(
            self.verificar_login
        )

    def verificar_login(self):

        # Pega o usuário digitado
        usuario = self.txt_usuario.text()

        # Pega a senha digitada
        senha = self.txt_senha.text()

        # Login temporário
        if usuario == "admin" and senha == "1234":

            print("Login realizado com sucesso!")

            # Envia o sinal para a página principal
            self.login_sucesso.emit()

        else:

            print("Usuário ou senha incorretos!")

            QtWidgets.QMessageBox.warning(
                self,
                "Erro de Login",
                "Usuário ou senha incorretos!"
            )

            # Limpa o campo de senha
            self.txt_senha.clear()