import sys
from PyQt5.QtWidgets import QApplication
from pagina_principal import TelaPrincipal


def main():
    app = QApplication(sys.argv)

    janela = TelaPrincipal()
    janela.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()