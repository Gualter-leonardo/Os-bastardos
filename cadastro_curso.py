from PyQt5 import QtWidgets, uic
import mysql.connector
import os


class TelaCadastroCursoAlt(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi(os.path.join(os.path.dirname(__file__), "tela", "cadastrarcurso.ui"), self)

        self.btn_cadastrar.clicked.connect(self.salvar_cadastro)

        self.conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )

        self.cursor = self.conexao.cursor()

    def salvar_cadastro(self):
        carga_horaria = self.txt_tempo.text()
        curso = self.txt_nome_curso.text()
        instrutor = self.txt_instrutor.text()
        quantidade_uc = self.txt_quantidade_uc.text()
        inicio = self.txt_inicio.text()

        if not carga_horaria or not curso:
            QtWidgets.QMessageBox.warning(self, "Erro", "Preencha os campos obrigatórios!")
            return

        try:
            comando = """
                INSERT INTO cursos2
                (carga_horaria, curso, instrutor, quantidade_uc, inicio)
                VALUES (%s, %s, %s, %s, %s)
            """

            dados = (carga_horaria, curso, instrutor, quantidade_uc, inicio)

            self.cursor.execute(comando, dados)
            self.conexao.commit()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "Curso cadastrado com sucesso"
            )

            self.txt_tempo.clear()
            self.txt_nome_curso.clear()
            self.txt_instrutor.clear()
            self.txt_quantidade_uc.clear()
            self.txt_inicio.clear()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))