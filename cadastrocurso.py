from PyQt5 import QtWidgets, uic
import conexao
import os


class TelaCadastroCurso(QtWidgets.QWidget):
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

        self.btn_cadastrar.clicked.connect(self.salvar_cadastro)

    def salvar_cadastro(self):
        carga_horaria = self.txt_tempo.text().strip()
        curso = self.txt_nome_curso.text().strip()
        instrutor = self.txt_instrutor.text().strip()
        quantidade_uc = self.txt_quantidade_uc.text().strip()
        inicio = self.txt_inicio.text().strip()

        if not curso or not quantidade_uc:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "Preencha o nome do curso e a quantidade de UCs."
            )
            return

        try:
            quantidade_uc = int(quantidade_uc)
            if quantidade_uc <= 0:
                raise ValueError
        except ValueError:
            QtWidgets.QMessageBox.warning(
                self,
                "Atenção",
                "A quantidade de UCs deve ser um número inteiro maior que zero."
            )
            return

        conn = None
        cursor = None

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO cursos2
                (carga_horaria, curso, instrutor, quantidade_uc, inicio)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    carga_horaria,
                    curso,
                    instrutor,
                    quantidade_uc,
                    inicio
                )
            )

            conn.commit()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "Curso cadastrado com sucesso!"
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
        self.txt_tempo.clear()
        self.txt_nome_curso.clear()
        self.txt_instrutor.clear()
        self.txt_quantidade_uc.clear()
        self.txt_inicio.clear()
