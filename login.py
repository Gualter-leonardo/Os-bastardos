import os
from PyQt5 import uic, QtCore, QtWidgets
import mysql.connector
import conexao

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class TelaLogin(QtWidgets.QMainWindow):
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        caminho = os.path.join(BASE_DIR, "tela", "login.ui")
        uic.loadUi(caminho, self)

        self.btn_entrar.clicked.connect(self.verificar_login)
        self.txt_senha.returnPressed.connect(self.verificar_login)
        self.txt_senha.setEchoMode(QtWidgets.QLineEdit.Password)

    def verificar_login(self):
        usuario = self.txt_usuario.text().strip()
        senha = self.txt_senha.text()

        if not usuario or not senha:
            QtWidgets.QMessageBox.warning(
                self,
                "Erro de Login",
                "Informe o usuário e a senha!"
            )
            return

        conn = None
        cursor = None
        try:
            conn = conexao.conectar()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, usuario FROM informacao WHERE usuario = %s AND senha = %s LIMIT 1",
                (usuario, senha)
            )
            resultado = cursor.fetchone()

            if resultado:
                self.login_sucesso.emit()
            else:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Erro de Login",
                    "Usuário ou senha incorretos!"
                )
                self.txt_senha.clear()
                self.txt_senha.setFocus()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Erro no banco de dados",
                f"Não foi possível consultar o login:\n\n{e}"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
