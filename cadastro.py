import sys
from PyQt5 import uic, QtWidgets

import conexao
import cadastro_uc
import curso


def salvar_cadastro():
    carga_horaria = tela.txt_carga_horaria.text()
    nome_curso = tela.txt_curso.text()
    instrutor = tela.txt_instrutor.text()
    quantidade_uc = tela.txt_quantidade.text()
    inicio = tela.txt_inicio.text()

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
        tela, "Sucesso", "Curso cadastrado com sucesso"
    )

    tela.txt_carga_horaria.setText("")
    tela.txt_curso.setText("")
    tela.txt_instrutor.setText("")
    tela.txt_quantidade.setText("")
    tela.txt_inicio.setText("")


def salvar_uc():
    cadastro_uc.salvar_uc()


def carregar_cursos():
    curso.carregar_cursos(tela)


# APP
app = QtWidgets.QApplication(sys.argv)

tela = uic.loadUi("tela/cadastrarcurso.ui")

tela.btn_cadastrar.clicked.connect(salvar_cadastro)

# se tiver botão de atualizar lista
if hasattr(tela, "btn_carregar"):
    tela.btn_carregar.clicked.connect(carregar_cursos)

tela.show()
sys.exit(app.exec())