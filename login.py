import mysql.connector
from PyQt5 import uic, QtCore, QtWidgets
import conexao

class TelaLogin(QtWidgets.QWidget):
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        uic.loadUi("tela/login.ui", self)
        self.setWindowTitle("Login")
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.Window)
        self.btn_login.clicked.connect(self.verificar_login)

    def verificar_login(self):
        usuario = self.txt_usuario.text()
        senha = self.txt_senha.text()

        comando = "SELECT * FROM informacao WHERE usuario=%s AND senha=%s"
        dados = (usuario, senha)

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()
            cursor.execute(comando, dados)
            resultado = cursor.fetchone()
        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))
            return
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

        if resultado:
            QtWidgets.QMessageBox.information(self, "Login", "Login realizado com sucesso")
            self.login_sucesso.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Login", "Usuário ou senha incorretos")
        
