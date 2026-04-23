import sys
from PyQt5 import uic, QtWidgets
import conexao


def carregar_cursos():
    conn = conexao.conectar()
    cursor = conn.cursor()

    comando = "SELECT DISTINCT curso FROM cursos2"
    cursor.execute(comando)

    resultados = cursor.fetchall()

    tela.comboBox.clear()

    for curso in resultados:
        tela.comboBox.addItem(curso[0])

    cursor.close()
    conn.close()


app = QtWidgets.QApplication(sys.argv)

tela = uic.loadUi("tela/cadastrarcurso.ui")

carregar_cursos()

tela.show()
sys.exit(app.exec())