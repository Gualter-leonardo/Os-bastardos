import sys
import mysql.connector
from PyQt5 import uic, QtWidgets

import conexao

def carregar_cursos():
    cursor = conexao.conexao.cursor()

    comando = "SELECT DISTINCT curso FROM cursos2"
    cursor.execute(comando)

    resultados = cursor.fetchall()

    tela.comboBox.clear()

    for curso in resultados:
        tela.comboBox.addItem(curso[0])

    cursor.close()


app = QtWidgets.QApplication(sys.argv)  # ✅ PRIMEIRO

tela = uic.loadUi("tela/cadastrarcurso.ui")  # ✅ depois

carregar_cursos()  # agora pode usar a tela

tela.show()

sys.exit(app.exec_())  # ✅ inicia o loop