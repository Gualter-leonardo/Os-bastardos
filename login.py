import sys

from PyQt5 import QtWidgets, QtCore


class TelaLogin(QtWidgets.QWidget):

    # Sinal enviado quando o login for realizado
    login_sucesso = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setFixedSize(400, 300)

        # ==========================================
        # LAYOUT PRINCIPAL
        # ==========================================

        layout = QtWidgets.QVBoxLayout()

        # ==========================================
        # TÍTULO
        # ==========================================

        titulo = QtWidgets.QLabel("LOGIN")
        titulo.setAlignment(QtCore.Qt.AlignCenter)

        titulo.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)

        layout.addWidget(titulo)

        # ==========================================
        # USUÁRIO
        # ==========================================

        self.txt_usuario = QtWidgets.QLineEdit()
        self.txt_usuario.setPlaceholderText("Usuário")

        self.txt_usuario.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)

        layout.addWidget(self.txt_usuario)

        # ==========================================
        # SENHA
        # ==========================================

        self.txt_senha = QtWidgets.QLineEdit()
        self.txt_senha.setPlaceholderText("Senha")

        self.txt_senha.setEchoMode(
            QtWidgets.QLineEdit.Password
        )

        self.txt_senha.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 14px;
            }
        """)

        layout.addWidget(self.txt_senha)

        # ==========================================
        # BOTÃO ENTRAR
        # ==========================================

        self.btn_entrar = QtWidgets.QPushButton("ENTRAR")

        self.btn_entrar.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #dddddd;
            }
        """)

        self.btn_entrar.clicked.connect(
            self.verificar_login
        )

        layout.addWidget(self.btn_entrar)

        # ==========================================
        # MENSAGEM
        # ==========================================

        self.lbl_mensagem = QtWidgets.QLabel("")
        self.lbl_mensagem.setAlignment(
            QtCore.Qt.AlignCenter
        )

        layout.addWidget(self.lbl_mensagem)

        # ==========================================
        # APLICAR LAYOUT
        # ==========================================

        self.setLayout(layout)

    # ==========================================
    # VERIFICAR LOGIN
    # ==========================================

    def verificar_login(self):

        usuario = self.txt_usuario.text()
        senha = self.txt_senha.text()

        # LOGIN TEMPORÁRIO

        if usuario == "admin" and senha == "1234":

            self.lbl_mensagem.setText(
                "Login realizado com sucesso!"
            )

            # Envia sinal para pagina_principal.py
            self.login_sucesso.emit()

        else:

            self.lbl_mensagem.setText(
                "Usuário ou senha incorretos!"
            )

            self.txt_senha.clear()


# ==========================================
# TESTAR LOGIN DIRETAMENTE
# ==========================================

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    janela = TelaLogin()
    janela.show()

    sys.exit(app.exec_())