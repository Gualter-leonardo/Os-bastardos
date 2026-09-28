from PyQt5 import QtWidgets


class TelaCursos(QtWidgets.QWidget):
    """Compatibilidade para o código antigo; a listagem fica no relatório da principal."""
    def __init__(self, principal=None):
        super().__init__(principal)
        self.principal = principal

    def carregar_cursos(self):
        if self.principal:
            self.principal.carregar_relatorio()

    def atualizar(self):
        self.carregar_cursos()
