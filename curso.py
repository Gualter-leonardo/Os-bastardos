import sys
from PyQt5 import uic, QtWidgets
import conexao
import os


class TelaCursos(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "tela", "cadastrarcurso.ui"), self)
        self.carregar_cursos()

    def carregar_cursos(self):
        try:
            conn = conexao.conectar()
            cursor = conn.cursor()

            comando = "SELECT DISTINCT curso FROM cursos2"
            cursor.execute(comando)

            resultados = cursor.fetchall()

            self.comboBox.clear()

            for curso in resultados:
                self.comboBox.addItem(curso[0])

            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar cursos: {e}")




