import sys
from PyQt5 import QtWidgets
from cadastro import CadastroCurso

app = QtWidgets.QApplication(sys.argv)

janela = CadastroCurso()
janela.show()

sys.exit(app.exec())