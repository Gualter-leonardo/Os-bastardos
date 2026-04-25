import sys
import mysql.connector
from PyQt5 import uic, QtWidgets


def verificar_login():
    
    usuario = tela.txt_usuario.text()
    senha = tela.txt_senha.text()
    
    QtWidgets.QMessageBox.information(tela, "Login", "Login realizado com sucesso")
    # conexao = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="",
    #     database="test"
    # )
    # cursor = conexao.cursor()
    
    # comando = "SELECT * FROM informacao WHERE usuario=%s AND senha=%s"
    # dados = (usuario, senha)
    # cursor.execute(comando, dados)
    # resultado = cursor.fetchone()
    # if resultado:

        
    # else:

    #     QtWidgets.QMessageBox.warning(tela, "Erro", "Usuario ou senha inválidos")

app = QtWidgets.QApplication([])
tela = uic.loadUi("tela/cadastrarcurso.ui")
# tela.btn_login.clicked.connect(verificar_login)
tela.show()
app.exec()
        
