from PyQt5 import QtWidgets


class TelaCadastroCurso(QtWidgets.QWidget):
    """Compatibilidade para o código antigo: o cadastro agora fica na tela principal."""
    def __init__(self, principal=None):
        super().__init__(principal)
        self.principal = principal
        if principal is not None:
            self.setWindowTitle("Cadastro de Curso")

    def salvar_cadastro(self):
        if self.principal:
            self.principal.salvar_curso()
