import sys
from PyQt5 import QtWidgets
from cadastro import CadastroCurso

print("antes app")

app = QtWidgets.QApplication(sys.argv)

print("antes janela")

janela = CadastroCurso()

print("depois janela")

janela.show()

print("show chamado")

sys.exit(app.exec())