from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic
import sys


# =========================
# TELA PRINCIPAL
# =========================
class TelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/principal.ui", self)

        self.btn_cadastro.clicked.connect(self.abrir_cadastro)
        self.btn_relatorio.clicked.connect(self.abrir_relatorio)
        self.btn_calendario.clicked.connect(self.abrir_calendario)
        self.btn_legenda.clicked.connect(self.abrir_legenda)

        self.janelas = []

    def abrir_janela(self, janela):
        janela.show()
        self.janelas.append(janela)

    def abrir_cadastro(self):
        self.abrir_janela(TelaCadastro())

    def abrir_relatorio(self):
        self.abrir_janela(TelaRelatorio())

    def abrir_calendario(self):
        self.abrir_janela(TelaCalendario())

    def abrir_legenda(self):
        self.abrir_janela(TelaLegenda())


# =========================
# TELA CADASTRO
# =========================
class TelaCadastro(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/cadastrarcurso.ui", self)


# =========================
# TELA RELATÓRIO
# =========================
class TelaRelatorio(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/relatorio.ui", self)


# =========================
# TELA CALENDÁRIO
# =========================
class TelaCalendario(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/calendario.ui", self)


# =========================
# TELA LEGENDA
# =========================
class TelaLegenda(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/legenda.ui", self)


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    sys.exit(app.exec_())