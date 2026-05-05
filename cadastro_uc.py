from PyQt5 import QtWidgets, uic
import conexao


class TelaCadastro(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("tela/cadastrarcurso.ui", self)

        self.btn_uc_cadastrar.clicked.connect(self.salvar_uc)

        self.conn = conexao.conectar()
        self.cursor = self.conn.cursor()

    def salvar_uc(self):
        horas_uc = self.txt_horasucs.text()
        posicao = self.txt_posicao.text()
        nome_uc = self.txt_nome_uc.text()

        if not horas_uc or not posicao or not nome_uc:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        try:
            comando = """
                INSERT INTO grade (horas_uc, posicao, nome_uc)
                VALUES (%s, %s, %s)
            """
            dados = (horas_uc, posicao, nome_uc)

            self.cursor.execute(comando, dados)
            self.conn.commit()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "Grade cadastrada com sucesso"
            )

            self.txt_horasucs.clear()
            self.txt_posicao.clear()
            self.txt_nome_uc.clear()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))