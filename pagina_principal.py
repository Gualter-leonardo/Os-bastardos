from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QWizardPage
from PyQt5 import uic
import sys


from conexao import salvar_cadastro, gerar_relatorio, configurar_calendario, carregar_legenda



# =========================
# CLASSE BASE PARA TELAS
# =========================
class BaseTela:
    def carregar_ui(self, caminho_ui):
        uic.loadUi(caminho_ui, self)


# =========================
# TELA PRINCIPAL
# =========================
class TelaPrincipal(QMainWindow, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/principal.ui")

        self.rotas = {
            self.btn_cadastro: TelaCadastro,
            self.btn_relatorio: TelaRelatorio,
            self.btn_calendario: TelaCalendario,
            self.btn_legenda: TelaLegenda
        }

        for botao, tela in self.rotas.items():
            botao.clicked.connect(lambda _, t=tela: self.abrir_janela(t))

        self.janelas = {}

    def abrir_janela(self, classe_tela):
        if classe_tela not in self.janelas:
            self.janelas[classe_tela] = classe_tela()

        self.janelas[classe_tela].show()
        self.janelas[classe_tela].raise_()


# =========================
# TELA CADASTRO
# =========================
class TelaCadastro(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/cadastrarcurso.ui")

        if hasattr(self, "btn_salvar"):
            self.btn_salvar.clicked.connect(self.executar_salvar)

    def executar_salvar(self):
        nome = self.input_nome.text() if hasattr(self, "input_nome") else ""
        curso = self.input_curso.text() if hasattr(self, "input_curso") else ""

        salvar_cadastro(nome, curso)


# =========================
# TELA RELATÓRIO
# =========================
class TelaRelatorio(QWizardPage, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/relatorio.ui")

        self.carregar_relatorio()

    def carregar_relatorio(self):
        gerar_relatorio()


# =========================
# TELA CALENDÁRIO
# =========================
class TelaCalendario(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/calendario.ui")

        self.configurar()

    def configurar(self):
        configurar_calendario()


# =========================
# TELA LEGENDA
# =========================
class TelaLegenda(QWizardPage, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/legenda.ui")

        self.carregar()

    def carregar(self):
        carregar_legenda()


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    sys.exit(app.exec_())