import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWizardPage
import conexao

class Main(QWizardPage):
    def __init__(self):
        super().__init__()

        uic.loadUi("tela/legenda.ui", self)
        self.btn_adicionar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        print("Feriado:", self.txt_feriado.text())
        print("Recesso:", self.txt_recesso.text())
        print("Estágio:", self.txt_estagio.text())
        print("Reunião:", self.txt_reuniao.text())
        print("Aula inaugural:", self.txt_aula_inaugural.text())

        print("Data início:", self.data_inicial.date().toString("dd/MM/yyyy"))
        print("Data fim:", self.data_final.date().toString("dd/MM/yyyy"))

        print("---- DADOS SALVOS ----")
