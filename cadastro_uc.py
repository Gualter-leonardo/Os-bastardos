import sys
import mysql.connector
from PyQt5 import uic, QtWidgets
import conexao
print(dir(conexao))


def salvar_uc():
    
    
    horas_uc = tela.txt_horasucs.text()
    posicao = tela.txt_posicao.text()
    nome_uc= tela.txt_nome_uc.text()

 # Cria o cursor que executa comandos SQL
    cursor = conexao.cursor()
    # Comando SQL de inserção
    comando = "INSERT INTO grade ( horas_uc, posicao, nome_uc) VALUES (%s,%s,%s)"\

    # Valores que serão inseridos
    dados = ( horas_uc, posicao ,nome_uc)
    # Executa o comando
    cursor.execute(comando, dados)
    # Confirma a alteração no banco
    conexao.commit()
    # Mostra mensagem para o usúario
    QtWidgets.QMessageBox.information(tela, "Sucesso","Grade cadastrada com sucesso")
    # Limpa os campos da tela
    
    tela.txt_horasucs.setText("")
    tela.txt_posicao.setText("")
    tela.txt_nome_uc.setText("")

# Inicialização da aplicação
app = QtWidgets.QApplication([])
# Carrega a interface criada no QtDesigner
tela = uic.loadUi("tela/cadastrarcurso.ui")
# Conecta o botão salvar com a função salvar_aluno
tela.btn_cadastrar_uc.clicked.connect(salvar_uc)

     
    