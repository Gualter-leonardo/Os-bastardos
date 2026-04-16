import sys
import mysql.connector
from PyQt5 import uic, QtWidgets

app = QtWidgets.QApplication([])
tela = uic.loadUi("tela/relatorio.ui")

def gerar_relatorio():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )

    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id_curso, curso, carga_horaria, instrutor
        FROM cursos2
    """)

    dados = cursor.fetchall()

    tela.txt_tabela.setRowCount(len(dados))
    tela.txt_tabela.setColumnCount(4)
    tela.txt_tabela.setHorizontalHeaderLabels(
        ["ID", "CURSO", "CARGA HORÁRIA", "INSTRUTOR"]
    )

    for linha, row_data in enumerate(dados):
        for coluna, valor in enumerate(row_data):
            tela.txt_tabela.setItem(
                linha, coluna, QtWidgets.QTableWidgetItem(str(valor))
            )

    cursor.close()
    conexao.close()

tela.btn_carregar.clicked.connect(gerar_relatorio)

tela.show()
app.exec()