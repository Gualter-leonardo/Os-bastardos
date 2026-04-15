import sys
import mysql.connector
from PyQt5 import uic, QtWidgets

import conexao  # precisa ter conexao = mysql.connector.connect(...)

def salvar_uc():
    valor_combo = tela.comboBox.currentText()

    cursor = conexao.conexao.cursor()  # pega conexão do arquivo conexao.py

    comando = "SELECT * FROM cursos2 WHERE curso = %s"
    cursor.execute(comando, (valor_combo,))

    resultados = cursor.fetchall()
    print(resultados)

    conexao.conexao.commit()
    cursor.close()
    conexao.conexao.close()


# Inicialização da aplicação
app = QtWidgets.QApplication([])

# Carrega interface
tela = uic.loadUi("tela/cadastrarcurso.ui")

# Conecta botão
tela.btn_cadastrar_uc.clicked.connect(salvar_uc)

# Mostra tela
tela.show()

app.exec()

#tste