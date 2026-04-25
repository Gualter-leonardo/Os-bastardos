import sys
import mysql.connector
from PyQt5 import uic, QtWidgets
import conexao

print(dir(conexao))


def salvar_uc():
    horas_uc = tela.txt_horasucs.text()
    posicao = tela.txt_posicao.text()
    nome_uc = tela.txt_nome_uc.text()

    conn = conexao.conectar()
    cursor = conn.cursor()

    comando = "INSERT INTO grade (horas_uc, posicao, nome_uc) VALUES (%s, %s, %s)"
    dados = (horas_uc, posicao, nome_uc)

    cursor.execute(comando, dados)
    conn.commit()

    QtWidgets.QMessageBox.information(tela, "Sucesso", "Grade cadastrada com sucesso")

    tela.txt_horasucs.setText("")
    tela.txt_posicao.setText("")
    tela.txt_nome_uc.setText("")


app = QtWidgets.QApplication([])

tela = uic.loadUi("tela/cadastrarcurso.ui")

tela.btn_cadastrar_uc.clicked.connect(salvar_uc)

tela.show()

sys.exit(app.exec())