import sys
import mysql.connector
from PyQt5 import uic, QtWidgets


def conectar():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )


def listar():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM test")

    dados = cursor.fetchall()

    tela.tabela_alunos.setRowCount(len(dados))

    for i in range (len(dados)):

        for j in range(4):

            tela.tabela_alunos.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados[i][j])))



app = QtWidgets.QApplication([])

tela = uic.loadUi("pagina_principal.ui")


tela.btn_listar.clicked.connect(listar)


tela.show()

app.exec()

