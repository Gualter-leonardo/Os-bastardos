from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5 import uic, QtCore
import sys
import os

from cadastro import TelaCadastroCurso
from relatorio import TelaRelatorio
from calendario import CalendarioApp
from legenda import Main as TelaLegenda

BASE_DIR = os.path.dirname(__file__)


# =========================
# CLASSE BASE PARA TELAS
# =========================
class BaseTela:
    def carregar_ui(self, caminho_ui):
        caminho = os.path.join(BASE_DIR, caminho_ui)
        uic.loadUi(caminho, self)


# =========================
# TELA PRINCIPAL
# =========================
class TelaPrincipal(QMainWindow, BaseTela):
    def __init__(self):
        super().__init__()
        print("Carregando UI principal")
        self.carregar_ui("tela/principal.ui")
        print("UI carregada")

        self.janelas = {}

        self.btn_cadastro.clicked.connect(lambda: self.abrir_janela(TelaCadastroCurso))
        self.btn_relatorio.clicked.connect(lambda: self.abrir_janela(TelaRelatorio))
        self.btn_calendario.clicked.connect(lambda: self.abrir_janela(TelaCalendario))
        self.btn_legenda.clicked.connect(lambda: self.abrir_janela(TelaLegenda))
        print("Conexoes feitas")

    def abrir_janela(self, classe_tela):
        # garante que a janela ainda existe
        janela = self.janelas.get(classe_tela)

        if janela is None:
            janela = classe_tela()

            # importante: evita crash ao fechar manualmente
            janela.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

            janela.destroyed.connect(lambda: self.janelas.pop(classe_tela, None))
            self.janelas[classe_tela] = janela

        janela.show()
        janela.raise_()
        janela.activateWindow()


# =========================
# TELA CALENDÁRIO
# =========================
class TelaCalendario(CalendarioApp):
    pass




# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    janela = TelaPrincipal()
    janela.show()

    sys.exit(app.exec_())