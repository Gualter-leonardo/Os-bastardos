from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCursos(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        # =====================================
        # CARREGAR A INTERFACE
        # =====================================

        caminho = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "curso.ui"
        )

        uic.loadUi(caminho, self)

        # =====================================
        # CARREGAR CURSOS DO BANCO
        # =====================================

        self.carregar_cursos()

    # =========================================
    # CARREGAR CURSOS
    # =========================================

    def carregar_cursos(self):

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
                """
            )

            resultados = cursor.fetchall()

            # =================================
            # CONFIGURAR TABELA
            # =================================

            self.tableWidget.clearContents()

            self.tableWidget.setRowCount(
                len(resultados)
            )

            self.tableWidget.setColumnCount(6)

            self.tableWidget.setHorizontalHeaderLabels([
                "ID",
                "Curso",
                "Qtd UCs",
                "Carga Horária",
                "Início",
                "Instrutor"
            ])

            # =================================
            # PREENCHER TABELA
            # =================================

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

            # =================================
            # AJUSTAR COLUNAS
            # =================================

            self.tableWidget.resizeColumnsToContents()

            cursor.close()
            conn.close()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                f"Erro ao carregar os cursos:\n\n{e}"
            )

    # =========================================
    # ATUALIZAR TELA
    # =========================================

    def atualizar(self):

        self.carregar_cursos()

    # =========================================
    # FECHAR
    # =========================================

    def closeEvent(self, event):

        event.accept()