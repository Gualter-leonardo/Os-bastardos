import sys
from PyQt5 import uic, QtWidgets
import conexao
import os


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



tela = uic.loadUi(os.path.join(os.path.dirname(__file__), "tela", "cadastrarcurso.ui"))




