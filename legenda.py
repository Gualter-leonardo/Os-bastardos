import sys
from PyQt5.QtWidgets import QApplication, QMainWindow , QWizardPage
import conexao 

class Main(QWizardPage):
    def __init__(self):
        super().__init__()

        self.ui = Ui_WizardPage()
        self.ui.setupUi(self)

        
        self.ui.btn_onar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        print("Feriado:", self.ui.txt_feriado.text())
        print("Recesso:", self.ui.txt_recesso.text())
        print("Estágio:", self.ui.txt_estagio.text())
        print("Reunião:", self.ui.txt_reuniao.text())
        print("Aula inaugural:", self.ui.txt_aula_inaugural.text())

        print("Data início:",
              self.ui.data_inicial.date().toString("dd/MM/yyyy"))
        print("Data fim:",
              self.ui.data_final.date().toString("dd/MM/yyyy"))

        print("---- DADOS SALVOS ----")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Main()
    janela.show()
    sys.exit(app.exec_())