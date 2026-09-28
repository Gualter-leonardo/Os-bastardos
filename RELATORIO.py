from PyQt5 import QtWidgets


class TelaRelatorio(QtWidgets.QWidget):
    """Compatibilidade para o código antigo; o relatório está em principal.ui."""
    def __init__(self, principal=None):
        super().__init__(principal)
        self.principal = principal

    def gerar_relatorio(self):
        if self.principal:
            self.principal.carregar_relatorio()
