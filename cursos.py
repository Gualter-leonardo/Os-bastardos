from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCursos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "curso.ui"
        )

        uic.loadUi(caminho, self)
        self.carregar_cursos()

    def carregar_cursos(self):
        conn = None
        cursor = None

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    id_curso,
                    curso,
                    quantidade_uc,
                    carga_horaria,
                    inicio,
                    instrutor
                FROM cursos2
                ORDER BY id_curso DESC
                """
            )

            resultados = cursor.fetchall()

            self.tableWidget.clearContents()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setRowCount(len(resultados))

            self.tableWidget.setHorizontalHeaderLabels([
                "ID",
                "Curso",
                "Qtd UCs",
                "Carga Horária",
                "Início",
                "Instrutor"
            ])

            for linha, row in enumerate(resultados):
                for coluna, valor in enumerate(row):
                    self.tableWidget.setItem(
                        linha,
                        coluna,
                        QtWidgets.QTableWidgetItem(
                            "" if valor is None else str(valor)
                        )
                    )

            self.tableWidget.resizeColumnsToContents()

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar os cursos:\n\n{e}"
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def atualizar(self):
        self.carregar_cursos()

    def closeEvent(self, event):
        event.accept()
