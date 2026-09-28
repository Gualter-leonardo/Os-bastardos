from PyQt5 import QtWidgets


class TelaLegenda(QtWidgets.QWidget):
    """Compatibilidade para o código antigo; a tela real está em principal.ui."""
    def __init__(self, principal=None):
        super().__init__(principal)
        self.principal = principal

    def salvar_dados(self):
        if self.principal:
            self.principal.salvar_legendas()
