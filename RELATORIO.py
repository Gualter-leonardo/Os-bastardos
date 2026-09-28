import mysql.connector
from PyQt5 import uic, QtWidgets
import os


class TelaRelatorio(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "relatorio.ui"
        )

        uic.loadUi(ui_path, self)

        self.btn_carregar.clicked.connect(self.gerar_relatorio)

    def gerar_relatorio(self):
        conexao = None
        cursor = None

        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sistema_cursos"
            )

            cursor = conexao.cursor()

            cursor.execute(
                """
                SELECT
                    id_curso,
                    curso,
                    carga_horaria,
                    instrutor
                FROM cursos2
                ORDER BY id_curso DESC
                """
            )

            dados = cursor.fetchall()

            self.txt_tabela.clearContents()
            self.txt_tabela.setRowCount(len(dados))
            self.txt_tabela.setColumnCount(4)

            self.txt_tabela.setHorizontalHeaderLabels([
                "ID",
                "CURSO",
                "CARGA HORÁRIA",
                "INSTRUTOR"
            ])

            for linha, row_data in enumerate(dados):
                for coluna, valor in enumerate(row_data):
                    self.txt_tabela.setItem(
                        linha,
                        coluna,
                        QtWidgets.QTableWidgetItem(
                            "" if valor is None else str(valor)
                        )
                    )

            self.txt_tabela.resizeColumnsToContents()

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Erro no banco",
                str(e)
            )

        finally:
            if cursor:
                cursor.close()
            if conexao:
                conexao.close()
