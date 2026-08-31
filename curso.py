from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCursos(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.join(
                os.path.dirname(__file__),
                "tela",
                "curso.ui"
            ),
            self
        )

        self.carregar_cursos()

    def carregar_cursos(self):

        try:

            conn = conexao.conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    curso,
                    quantidade_uc,
                    carga_horaria,
                    inicio,
                    instrutor
                FROM cursos2
                """
            )

            resultados = cursor.fetchall()

            self.tableWidget.setRowCount(
                len(resultados)
            )

            self.tableWidget.setColumnCount(5)

            self.tableWidget.setHorizontalHeaderLabels([
                "Curso",
                "Qtd UCs",
                "Carga horária",
                "Início",
                "Instrutor"
            ])

            for linha, row in enumerate(resultados):

                for coluna, valor in enumerate(row):

                    item = QtWidgets.QTableWidgetItem(
                        str(valor)
                    )

                    self.tableWidget.setItem(
                        linha,
                        coluna,
                        item
                    )

            self.tableWidget.resizeColumnsToContents()

            cursor.close()
            conn.close()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar cursos:\n{e}"
            )

    def atualizar(self):
        self.carregar_cursos()
