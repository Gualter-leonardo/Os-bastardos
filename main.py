import sys
from PyQt5.QtWidgets import QApplication
from login import TelaLogin



def main():
    try:
        app = QApplication(sys.argv)

        login = TelaLogin()
        

        login.show()
        login.raise_()
        login.activateWindow()

        sys.exit(app.exec_())

    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()