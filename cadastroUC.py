from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCadastroUC(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Continua usando a UI que você já criou.
        uic.loadUi(
            os.path.join(
                os.path.dirname(__file__),
                "tela",
                "cadastrarcurso.ui"
            ),
            self
        )

        self.btn_uc_cadastrar.clicked.connect(self.salvar_uc)

    def salvar_uc(self):
        horas_uc = self.txt_horas_uc.text().strip()
        posicao = self.txt_posicao.text().strip()
        nome_uc = self.txt_nome_uc.text().strip()

        if not horas_uc or not posicao or not nome_uc:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha todos os campos da UC!"
            )
            return

        try:
            horas_uc = int(horas_uc)
            posicao = int(posicao)

            if horas_uc <= 0 or posicao <= 0:
                raise ValueError

        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Horas e posição devem ser números inteiros maiores que zero."
            )
            return

        conn = None
        cursor = None

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO grade
                (horas_uc, posicao, nome_uc)
                VALUES (%s, %s, %s)
                """,
                (horas_uc, posicao, nome_uc)
            )

            conn.commit()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "UC cadastrada com sucesso!"
            )

            self.txt_horas_uc.clear()
            self.txt_posicao.clear()
            self.txt_nome_uc.clear()

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
