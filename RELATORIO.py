import mysql.connector
from PyQt5 import uic, QtWidgets


class TelaRelatorio(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/relatorio.ui", self)

        self.btn_carregar.clicked.connect(self.gerar_relatorio)

    def gerar_relatorio(self):
        try:
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

            # limpa tabela antes de preencher
            self.txt_tabela.setRowCount(0)

            self.txt_tabela.setRowCount(len(dados))
            self.txt_tabela.setColumnCount(4)
            self.txt_tabela.setHorizontalHeaderLabels(
                ["ID", "CURSO", "CARGA HORÁRIA", "INSTRUTOR"]
            )

            for linha, row_data in enumerate(dados):
                for coluna, valor in enumerate(row_data):
                    self.txt_tabela.setItem(
                        linha,
                        coluna,
                        QtWidgets.QTableWidgetItem(str(valor))
                    )

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexao' in locals():
                conexao.close()