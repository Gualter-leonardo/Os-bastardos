import os
from PyQt5 import uic, QtCore, QtWidgets

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TelaLogin(QtWidgets.QMainWindow):
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        caminho = os.path.join(BASE_DIR, "tela", "login.ui")
        uic.loadUi(caminho, self)

        # Mantém os nomes que você já criou no Qt Designer.
        self.btn_entrar.clicked.connect(self.verificar_login)
        self.txt_senha.returnPressed.connect(self.verificar_login)
        self.txt_senha.setEchoMode(QtWidgets.QLineEdit.Password)

    def verificar_login(self):
        usuario = self.txt_usuario.text().strip()
        senha = self.txt_senha.text()

        if usuario == "admin" and senha == "1234":
            self.login_sucesso.emit()
        else:
            QtWidgets.QMessageBox.warning(
                self,
                "Erro de Login",
                "Usuário ou senha incorretos!"
            )
            self.txt_senha.clear()
            self.txt_senha.setFocus()
