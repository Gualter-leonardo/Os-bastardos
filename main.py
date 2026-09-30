import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox

from login import TelaLogin
from pagina_principal import TelaPrincipal


class Sistema:
    def __init__(self):
        self.app = QApplication(sys.argv)
        # A janela de login pode desaparecer sem encerrar o processo.
        self.app.setQuitOnLastWindowClosed(False)
        self.login = TelaLogin()
        self.principal = None

        self.login.login_sucesso.connect(
            lambda: QtCore.QTimer.singleShot(0, self.abrir_principal)
        )

    def abrir_principal(self):
        # Primeiro cria e exibe a tela principal.
        # Só fecha o login depois que a tela principal foi criada com sucesso.
        try:
            nova_tela = TelaPrincipal()
            nova_tela.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
            # Guardar a referência antes de exibir evita que o Python descarte
            # a janela ao sair deste método.
            self.principal = nova_tela
            nova_tela.showMaximized()
            nova_tela.raise_()
            nova_tela.activateWindow()
            if not nova_tela.isVisible():
                raise RuntimeError("A tela principal não ficou visível após show().")
            self.login.hide()

        except Exception as e:
            import traceback
            traceback.print_exc()
            # Se houver algum erro ao abrir a tela principal,
            # o login continua aberto para o usuário poder ver o erro.
            QMessageBox.critical(
                self.login,
                "Erro ao abrir o sistema",
                f"Não foi possível abrir a tela principal:\n\n{e}"
            )

    def executar(self):
        area = self.app.primaryScreen().availableGeometry()
        self.login.resize(
            min(self.login.width(), area.width()),
            min(self.login.height(), area.height()),
        )
        self.login.move(area.center() - self.login.rect().center())
        self.login.show()
        self.login.raise_()
        self.login.activateWindow()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    sistema = Sistema()
    sistema.executar()
