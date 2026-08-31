from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCadastroUC(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.join(
                os.path.dirname(__file__),
                "tela",
                "cadastrarcurso.ui"
            ),
            self
        )

        self.btn_uc_cadastrar.clicked.connect(self.salvar_uc)

        self.conn = None
        self.cursor = None

        try:
            self.conn = conexao.conectar()
            self.cursor = self.conn.cursor()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro de conexão",
                str(e)
            )

    def salvar_uc(self):

        horas_uc = self.txt_horasucs.text()
        posicao = self.txt_horasucs_2.text()
        nome_uc = self.txt_horasucs_3.text()

        if not horas_uc or not posicao or not nome_uc:

            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha todos os campos!"
            )

            return

        try:

            comando = """
                INSERT INTO grade
                (horas_uc, posicao, nome_uc)
                VALUES (%s, %s, %s)
            """

            dados = (
                horas_uc,
                posicao,
                nome_uc
            )

            self.cursor.execute(comando, dados)
            self.conn.commit()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "UC cadastrada com sucesso!"
            )

            self.txt_horasucs.clear()
            self.txt_horasucs_2.clear()
            self.txt_horasucs_3.clear()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def closeEvent(self, event):

        if self.conn:
            try:
                self.cursor.close()
                self.conn.close()
            except:
                pass

        event.accept()