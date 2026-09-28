from PyQt5 import QtCore, QtWidgets, uic
import conexao
import os


class TelaLegenda(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "legenda.ui"
        )

        uic.loadUi(caminho, self)

        # No seu .ui o botão existente é btn_legenda.
        self.btn_legenda.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        inicio = self.data_inicial.date()

        legendas = [
            ("FERIADO", self.txt_feriado.text().strip()),
            ("RECESSO", self.txt_recesso.text().strip()),
            ("PLANEJAMENTO", self.txt_planejamento.text().strip()),
            ("INICIO_CURSO", self.txt_aula_inaugural.text().strip()),
            ("CAPACITACAO", self.txt_capacitacao_orientador.text().strip()),
            ("REUNIAO", self.txt_reuniao.text().strip()),
            ("ESTAGIO", self.txt_estagio.text().strip()),
            ("FINAL_CURSO", self.txt_final_curso.text().strip())
        ]

        legendas = [
            (tipo, texto)
            for tipo, texto in legendas
            if texto
        ]

        if not legendas:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha ao menos um campo antes de adicionar."
            )
            return

        conn = None
        cursor = None

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            comando = """
                INSERT INTO legendas
                (ano, mes, dia, tipo, texto)
                VALUES (%s, %s, %s, %s, %s)
            """

            for tipo, texto in legendas:
                cursor.execute(
                    comando,
                    (
                        inicio.year(),
                        inicio.month(),
                        inicio.day(),
                        tipo,
                        texto
                    )
                )

            conn.commit()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "Legenda salva com sucesso."
            )

            self.limpar_campos()

        except Exception as e:
            if conn:
                conn.rollback()

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def limpar_campos(self):
        self.txt_feriado.clear()
        self.txt_recesso.clear()
        self.txt_planejamento.clear()
        self.txt_aula_inaugural.clear()
        self.txt_capacitacao_orientador.clear()
        self.txt_reuniao.clear()
        self.txt_estagio.clear()
        self.txt_final_curso.clear()

        self.data_inicial.setDate(QtCore.QDate.currentDate())

        if hasattr(self, "data_final"):
            self.data_final.setDate(QtCore.QDate.currentDate())
