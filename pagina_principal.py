from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys
import os

from login import TelaLogin
from cadastro_curso import TelaCadastroCurso
from cadastro_uc import TelaCadastroUC
from curso import TelaCursos
from calendario import CalendarioApp


BASE_DIR = os.path.dirname(__file__)


class TelaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        # =========================
        # CARREGA PRINCIPAL.UI
        # =========================

        caminho = os.path.join(
            BASE_DIR,
            "tela",
            "principal.ui"
        )

        uic.loadUi(caminho, self)

        # =========================
        # CRIA AS TELAS INTERNAS
        # =========================

        self.tela_curso = TelaCadastroCurso()
        self.tela_uc = TelaCadastroUC()
        self.tela_relatorio = TelaCursos()
        self.tela_calendario = CalendarioApp()

        # =========================
        # ADICIONA NO STACKEDWIDGET
        # =========================

        self.stackedWidget.addWidget(
            self.tela_curso
        )

        self.stackedWidget.addWidget(
            self.tela_uc
        )

        self.stackedWidget.addWidget(
            self.tela_relatorio
        )

        self.stackedWidget.addWidget(
            self.tela_calendario
        )

        # =========================
        # BOTÕES
        # =========================

        self.btn_cadastro.clicked.connect(
            self.abrir_cadastro
        )

        self.btn_uc.clicked.connect(
            self.abrir_uc
        )

        self.btn_relatorio.clicked.connect(
            self.abrir_relatorio
        )

        self.btn_calendario.clicked.connect(
            self.abrir_calendario
        )

        # começa no cadastro
        self.stackedWidget.setCurrentWidget(
            self.tela_curso
        )

    # =========================
    # NAVEGAÇÃO
    # =========================

    def abrir_cadastro(self):

        self.stackedWidget.setCurrentWidget(
            self.tela_curso
        )

    def abrir_uc(self):

        self.stackedWidget.setCurrentWidget(
            self.tela_uc
        )

    def abrir_relatorio(self):

        self.tela_relatorio.atualizar()

        self.stackedWidget.setCurrentWidget(
            self.tela_relatorio
        )

    def abrir_calendario(self):

        self.tela_calendario.atualizar_formatacao()

        self.stackedWidget.setCurrentWidget(
            self.tela_calendario
        )


# =========================
# SISTEMA
# =========================

class Sistema:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.login = TelaLogin()
        self.principal = TelaPrincipal()

        self.login.login_sucesso.connect(
            self.abrir_principal
        )

    def abrir_principal(self):

        self.login.close()

        self.principal.show()
        self.principal.raise_()
        self.principal.activateWindow()

    def executar(self):

        self.login.show()

        sys.exit(
            self.app.exec_()
        )


# =========================
# INICIAR
# =========================

if __name__ == "__main__":

    sistema = Sistema()
    sistema.executar()