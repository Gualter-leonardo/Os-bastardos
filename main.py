import sys
from PyQt5.QtWidgets import QApplication

from login import TelaLogin
from pagina_principal import TelaPrincipal


class Sistema:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.login = TelaLogin()
        self.principal = None

        self.login.login_sucesso.connect(
            self.abrir_principal
        )

    def abrir_principal(self):
        self.login.close()

        self.principal = TelaPrincipal()
        self.principal.show()

    def executar(self):
        self.login.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    sistema = Sistema()
    sistema.executar()
