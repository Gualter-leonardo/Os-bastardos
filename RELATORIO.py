import mysql.connector
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWizardPage
import os


class TelaRelatorio(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Carrega o arquivo UI do relatorio
            ui_path = os.path.join(os.path.dirname(__file__), "tela", "relatorio.ui")
            # Usa um container temporário para carregar a UI
            self.ui_container = QWizardPage()
            uic.loadUi(ui_path, self.ui_container)
            
            # Copia os widgets do container para esta janela
            if hasattr(self.ui_container, 'btn_carregar'):
                self.btn_carregar = self.ui_container.btn_carregar
                self.btn_carregar.clicked.connect(self.gerar_relatorio)
            
            if hasattr(self.ui_container, 'txt_tabela'):
                self.txt_tabela = self.ui_container.txt_tabela
                
        except Exception as e:
            print(f"Aviso: Usando UI simplificada para relatorio. Erro: {e}")
            # Criar UI programaticamente se não conseguir carregar do arquivo
            self.setWindowTitle("Relatório")

    def gerar_relatorio(self):
        try:
            conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="test"
            )

            cursor = conexao.cursor()

            cursor.execute("""
                SELECT id_curso, curso, carga_horaria, instrutor
                FROM cursos2
            """)

            dados = cursor.fetchall()

            # limpa tabela antes de preencher
            self.txt_tabela.setRowCount(0)

            self.txt_tabela.setRowCount(len(dados))
            self.txt_tabela.setColumnCount(4)
            self.txt_tabela.setHorizontalHeaderLabels(
                ["ID", "CURSO", "CARGA HORÁRIA", "INSTRUTOR"]
            )

            for linha, row_data in enumerate(dados):
                for coluna, valor in enumerate(row_data):
                    self.txt_tabela.setItem(
                        linha,
                        coluna,
                        QtWidgets.QTableWidgetItem(str(valor))
                    )

        except mysql.connector.Error as e:
            QtWidgets.QMessageBox.critical(self, "Erro no banco", str(e))

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conexao' in locals():
                conexao.close()