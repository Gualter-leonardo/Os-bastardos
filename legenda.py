from PyQt5 import QtCore, QtWidgets, uic
import conexao
import os

class TelaLegenda(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(os.path.dirname(__file__), "tela", "legenda.ui"), self)
        self.btn_adicionar.clicked.connect(self.salvar_dados)

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
        ]

        if not any(text for _, text in legendas):
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha ao menos um campo antes de adicionar.",
            )
            return

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            for tipo, texto in legendas:
                if not texto:
                    continue

                comando = (
                    "INSERT INTO legendas (ano, mes, dia, tipo, texto) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )
                cursor.execute(
                    comando,
                    (
                        inicio.year(),
                        inicio.month(),
                        inicio.day(),
                        tipo,
                        texto,
                    ),
                )

            conn.commit()
            cursor.close()
            conn.close()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "Legenda salva com sucesso.",
            )

            self.limpar_campos()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))

    def limpar_campos(self):
        self.txt_feriado.clear()
        self.txt_recesso.clear()
        self.txt_planejamento.clear()
        self.txt_aula_inaugural.clear()
        self.txt_capacitacao_orientador.clear()
        self.txt_reuniao.clear()
        self.txt_estagio.clear()
        self.data_inicial.setDate(QtCore.QDate.currentDate())
        self.data_final.setDate(QtCore.QDate.currentDate())
