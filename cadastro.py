from PyQt5 import QtWidgets, uic
import conexao


class TelaCadastroCurso(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("tela/cadastrarcurso.ui", self)

        self.btn_cadastrar.clicked.connect(self.salvar_cadastro)

    def salvar_cadastro(self):
        carga_horaria = self.txt_carga_horaria.text()
        nome_curso = self.txt_curso.text()
        instrutor = self.txt_instrutor.text()
        quantidade_uc = self.txt_quantidade.text()
        inicio = self.txt_inicio.text()

        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            comando = """
                INSERT INTO cursos2
                (carga_horaria, curso, instrutor, quantidade_uc, inicio)
                VALUES (%s, %s, %s, %s, %s)
            """

            dados = (carga_horaria, nome_curso, instrutor, quantidade_uc, inicio)

            cursor.execute(comando, dados)
            conn.commit()

            cursor.close()
            conn.close()

            QtWidgets.QMessageBox.information(
                self, "Sucesso", "Curso cadastrado com sucesso"
            )

            self.limpar_campos()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))

    def limpar_campos(self):
        self.txt_carga_horaria.clear()
        self.txt_curso.clear()
        self.txt_instrutor.clear()
        self.txt_quantidade.clear()
        self.txt_inicio.clear()