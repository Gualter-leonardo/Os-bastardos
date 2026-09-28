import os
from PyQt5 import uic, QtWidgets

from cadastrocurso import TelaCadastroCurso
from cadastroUC import TelaCadastroUC
from cursos import TelaCursos
from legenda import TelaLegenda
from relatorio import TelaRelatorio


class TelaPrincipal(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "principal.ui"
        )

        uic.loadUi(caminho, self)

        # Só conecte estes botões se eles realmente existirem
        # no seu principal.ui.
        if hasattr(self, "btn_cadastro_curso"):
            self.btn_cadastro_curso.clicked.connect(
                lambda: self.abrir_janela(TelaCadastroCurso)
            )

        if hasattr(self, "btn_cadastro_uc"):
            self.btn_cadastro_uc.clicked.connect(
                lambda: self.abrir_janela(TelaCadastroUC)
            )

        if hasattr(self, "btn_cursos"):
            self.btn_cursos.clicked.connect(
                lambda: self.abrir_janela(TelaCursos)
            )

        if hasattr(self, "btn_legenda"):
            self.btn_legenda.clicked.connect(
                lambda: self.abrir_janela(TelaLegenda)
            )

        if hasattr(self, "btn_relatorio"):
            self.btn_relatorio.clicked.connect(
                lambda: self.abrir_janela(TelaRelatorio)
            )

    def abrir_janela(self, classe):
        janela = classe()

        # Mantém a janela viva enquanto a principal estiver aberta.
        if not hasattr(self, "_janelas"):
            self._janelas = []

        self._janelas.append(janela)
        janela.show()
        janela.raise_()
        janela.activateWindow()
