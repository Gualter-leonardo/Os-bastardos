from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5 import uic
import sys


class pagina_principal(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("tela/principal.ui", self)

        self.btn_cadastro.clicked.connect(lambda: self.abrir("tela/cadastrarcurso.ui"))
        self.btn_relatorio.clicked.connect(lambda: self.abrir("tela/relatorio.ui"))
        self.btn_calendario.clicked.connect(lambda: self.abrir("tela/calendario.ui"))
        self.btn_legenda.clicked.connect(lambda: self.abrir("tela/legenda.ui"))

        self.janelas = []

    def abrir(self, caminho):
        janela = QWidget()
        uic.loadUi(caminho, janela)
        janela.show()
        self.janelas.append(janela)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = pagina_principal()
    janela.show()
    sys.exit(app.exec_())