import sys
import mysql.connector
from PyQt5 import uic, QtWidgets

# carregar interface
app = QtWidgets.QApplication([])
tela = uic.loadUi("relatorio.ui")

def gerar_relatorio():
    conexao = mysql.connect("test")
    cursor = conexao.cursor()

    # consulta
    cursor.execute("""
        SELECT id_curso, curso, carga_horaria, instrutor
        FROM cursos2
    """)

    dados = cursor.fetchall()

    # configurar tabela
    tela.txt_tabela.setRowCount(len(dados))
    tela.txt_tabela.setColumnCount(4)
    tela.txt_tabela.setHorizontalHeaderLabels(
        ["CURSO", "HORAS TOTAIS", "INSTRUTOR", "UC"]
    )

    # preencher tabela
    for linha, row_data in enumerate(dados):
        for coluna, valor in enumerate(row_data):
            tela.txt_tabela.setItem(
                linha, coluna, QtWidgets.QTableWidgetItem(str(valor))
            )

    conexao.close()

# botão
tela.btn_carregar.clicked.connect(btn_carregar)

tela.show()
app.exec()