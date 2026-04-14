import sys
import mysql.connector
# Importa classes principais do PyQt5
from PyQt5 import uic, QtWidgets

# Função que será executada quando clicar no botão salvar
def salvar_cadastro():
    # Pega os dados digitados nos campos da tela
    
    carga_horaria = tela.txt_tempo.text()
    curso = tela.txt_curso.text()
    instrutor = tela.txt_instrutor.text()
    quantidade_uc = tela.txt_quantidade.text()
    inicio = tela.txt_inicio.text()

    # Conexão com o banco de dados MySQL
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    # Cria o cursor que executa comandos SQL
    cursor = conexao.cursor()
    # Comando SQL de inserção
    comando = "INSERT INTO cursos2 ( carga_horaria, curso, instrutor, quantidade_uc, inicio) VALUES (%s,%s,%s,%s,%s)"\

    # Valores que serão inseridos
    dados = ( carga_horaria, curso ,instrutor, quantidade_uc, inicio)
    # Executa o comando
    cursor.execute(comando, dados)
    # Confirma a alteração no banco
    conexao.commit()
    # Mostra mensagem para o usúario
    QtWidgets.QMessageBox.information(tela, "Sucesso","Aluno cadastrado com sucesso")
    # Limpa os campos da tela
    
    tela.txt_carga_horaria.setText("")
    tela.txt_curso.setText("")
    tela.txt_instrutor.setText("")
    tela.txt_quantidade.setText("")
    tela.txt_inicio.setText("")

# Inicialização da aplicação
app = QtWidgets.QApplication([])
# Carrega a interface criada no QtDesigner
tela = uic.loadUi("cadastrarcurso.ui")
# Conecta o botão salvar com a função salvar_aluno
tela.btn_cadastrar.clicked.connect(salvar_cadastro)
# Mostra a tela
tela.show()
# Mantém o programa em execução
app.exec()