import sys
from PyQt5.QtWidgets import QApplication
from login import TelaLogin
from pagina_principal import TelaPrincipal


def main():
    app = QApplication(sys.argv)

    login = TelaLogin()
    janela = TelaPrincipal()

    def abrir_principal():
        login.close()
        janela.show()
        janela.raise_()
        janela.activateWindow()

    login.login_sucesso.connect(abrir_principal)
    login.show()
    login.raise_()
    login.activateWindow()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()