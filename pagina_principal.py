from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QWizardPage
from PyQt5 import uic
import sys


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

        # Mapeamento de botões → telas
        self.rotas = {
            self.btn_cadastro: TelaCadastro,
            self.btn_relatorio: TelaRelatorio,
            self.btn_calendario: TelaCalendario,
            self.btn_legenda: TelaLegenda
        }

        # Conectar todos os botões automaticamente
        for botao, tela in self.rotas.items():
            botao.clicked.connect(lambda _, t=tela: self.abrir_janela(t))

        self.janelas = {}

    def abrir_janela(self, classe_tela):
        # Evita recriar a janela se já existir
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

        # Exemplo de função conectada
        if hasattr(self, "btn_salvar"):
            self.btn_salvar.clicked.connect(self.salvar_dados)

    def salvar_dados(self):
        print("Dados salvos!")  # Aqui entra sua lógica


# =========================
# TELA RELATÓRIO
# =========================
class TelaRelatorio(QWizardPage, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/relatorio.ui")

        self.carregar_relatorio()

    def carregar_relatorio(self):
        print("Carregando relatório...")


# =========================
# TELA CALENDÁRIO
# =========================
class TelaCalendario(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/calendario.ui")

        self.configurar_calendario()

    def configurar_calendario(self):
        print("Calendário configurado!")


# =========================
# TELA LEGENDA
# =========================
class TelaLegenda(QWizardPage, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/legenda.ui")

        self.carregar_legenda()

    def carregar_legenda(self):
        print("Legenda carregada!")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = TelaPrincipal()
    janela.show()
    sys.exit(app.exec_())