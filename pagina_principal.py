import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

from login import TelaLogin
from cadastro_curso import TelaCadastroCurso
from cadastro_uc import TelaCadastroUC
from curso import TelaCursos
from calendario import CalendarioApp
from legenda import TelaLegenda
from relatorio import TelaRelatorio


# ==========================================
# DIRETÓRIO DO PROJETO
# ==========================================

BASE_DIR = os.path.dirname(__file__)


# ==========================================
# TELA PRINCIPAL
# ==========================================

class TelaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        # ==================================
        # CARREGAR PRINCIPAL.UI
        # ==================================

        caminho = os.path.join(
            BASE_DIR,
            "tela",
            "principal.ui"
        )

        uic.loadUi(
            caminho,
            self
        )

        # ==================================
        # CRIAR AS TELAS INTERNAS
        # ==================================

        self.tela_cadastro_curso = TelaCadastroCurso()

        self.tela_cadastro_uc = TelaCadastroUC()

        self.tela_cursos = TelaCursos()

        self.tela_calendario = CalendarioApp()

        self.tela_legenda = TelaLegenda()

        self.tela_relatorio = TelaRelatorio()

        # ==================================
        # ADICIONAR AS TELAS AO STACKED
        # ==================================

        self.stackedWidget.addWidget(
            self.tela_cadastro_curso
        )

        self.stackedWidget.addWidget(
            self.tela_cadastro_uc
        )

        self.stackedWidget.addWidget(
            self.tela_cursos
        )

        self.stackedWidget.addWidget(
            self.tela_calendario
        )

        self.stackedWidget.addWidget(
            self.tela_legenda
        )

        self.stackedWidget.addWidget(
            self.tela_relatorio
        )

        # ==================================
        # CONECTAR BOTÕES
        # ==================================

        self.btn_cadastro.clicked.connect(
            self.abrir_cadastro_curso
        )

        self.btn_uc.clicked.connect(
            self.abrir_cadastro_uc
        )

        self.btn_calendario.clicked.connect(
            self.abrir_calendario
        )

        self.btn_legenda.clicked.connect(
            self.abrir_legenda
        )

        self.btn_relatorio.clicked.connect(
            self.abrir_relatorio
        )

        self.btn_cursos.clicked.connect(
            self.abrir_cursos
        )

        # ==================================
        # TELA INICIAL
        # ==================================

        self.stackedWidget.setCurrentWidget(
            self.tela_cadastro_curso
        )

    # ======================================
    # CADASTRO DE CURSO
    # ======================================

    def abrir_cadastro_curso(self):

        self.stackedWidget.setCurrentWidget(
            self.tela_cadastro_curso
        )

    # ======================================
    # CADASTRO DE UC
    # ======================================

    def abrir_cadastro_uc(self):

        self.stackedWidget.setCurrentWidget(
            self.tela_cadastro_uc
        )

    # ======================================
    # CURSOS
    # ======================================

    def abrir_cursos(self):

        self.tela_cursos.atualizar()

        self.stackedWidget.setCurrentWidget(
            self.tela_cursos
        )

    # ======================================
    # CALENDÁRIO
    # ======================================

    def abrir_calendario(self):

        self.tela_calendario.atualizar_formatacao()

        self.stackedWidget.setCurrentWidget(
            self.tela_calendario
        )

    # ======================================
    # LEGENDA
    # ======================================

    def abrir_legenda(self):

        self.stackedWidget.setCurrentWidget(
            self.tela_legenda
        )

    # ======================================
    # RELATÓRIO
    # ======================================

    def abrir_relatorio(self):

        self.tela_relatorio.gerar_relatorio()

        self.stackedWidget.setCurrentWidget(
            self.tela_relatorio
        )


# ==========================================
# SISTEMA
# ==========================================

class Sistema:

    def __init__(self):

        # ==================================
        # CRIAR APLICAÇÃO
        # ==================================

        self.app = QApplication(sys.argv)

        # ==================================
        # CRIAR LOGIN
        # ==================================

        self.login = TelaLogin()

        # ==================================
        # CRIAR PRINCIPAL
        # ==================================

        self.principal = TelaPrincipal()

        # ==================================
        # SINAL DO LOGIN
        # ==================================

        self.login.login_sucesso.connect(
            self.abrir_principal
        )

    # ======================================
    # ABRIR PRINCIPAL
    # ======================================

    def abrir_principal(self):

        print(
            "Login realizado. Abrindo tela principal..."
        )

        # Fechar login

        self.login.close()

        # Mostrar principal

        self.principal.show()

        self.principal.raise_()

        self.principal.activateWindow()

    # ======================================
    # EXECUTAR
    # ======================================

    def executar(self):

        self.login.show()

        sys.exit(
            self.app.exec_()
        )


# ==========================================
# INICIAR PROGRAMA
# ==========================================

if __name__ == "__main__":

    sistema = Sistema()

    sistema.executar()