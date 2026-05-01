from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5 import uic
import sys
import os

from conexao import salvar_cadastro, gerar_relatorio, configurar_calendario, carregar_legenda


BASE_DIR = os.path.dirname(__file__)


# =========================
# CLASSE BASE PARA TELAS
# =========================
class BaseTela:
    def carregar_ui(self, caminho_ui):
        caminho = os.path.join(BASE_DIR, caminho_ui)
        uic.loadUi(caminho, self)


# =========================
# TELA PRINCIPAL
# =========================
class TelaPrincipal(QMainWindow, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/principal.ui")

        self.janelas = {}

        self.btn_cadastro.clicked.connect(lambda: self.abrir_janela(TelaCadastro))
        self.btn_relatorio.clicked.connect(lambda: self.abrir_janela(TelaRelatorio))
        self.btn_calendario.clicked.connect(lambda: self.abrir_janela(TelaCalendario))
        self.btn_legenda.clicked.connect(lambda: self.abrir_janela(TelaLegenda))

    def abrir_janela(self, classe_tela):
        if classe_tela not in self.janelas:
            janela = classe_tela()

            # Remove da memória ao fechar
            janela.destroyed.connect(lambda: self.janelas.pop(classe_tela, None))

            self.janelas[classe_tela] = janela

        self.janelas[classe_tela].show()
        self.janelas[classe_tela].raise_()
        self.janelas[classe_tela].activateWindow()


# =========================
# TELA CADASTRO
# =========================
class TelaCadastro(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/cadastrarcurso.ui")

        self.btn_cadastrar.clicked.connect(self.executar_salvar)

    def executar_salvar(self):
        nome = self.input_nome.text()
        curso = self.input_curso.text()

        if not nome or not curso:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos!")
            return

        try:
            salvar_cadastro(nome, curso)
            QMessageBox.information(self, "Sucesso", "Cadastro salvo com sucesso!")

            self.input_nome.clear()
            self.input_curso.clear()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar: {e}")


# =========================
# TELA RELATÓRIO
# =========================
class TelaRelatorio(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/relatorio.ui")

        self.carregar_relatorio()

    def carregar_relatorio(self):
        try:
            dados = gerar_relatorio()

            # Exemplo: se tiver um QListWidget chamado lista
            if hasattr(self, "lista"):
                self.lista.clear()
                for item in dados:
                    self.lista.addItem(str(item))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao gerar relatório: {e}")


# =========================
# TELA CALENDÁRIO
# =========================
class TelaCalendario(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/calendario.ui")

        self.configurar()

    def configurar(self):
        try:
            configurar_calendario(self)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro no calendário: {e}")


# =========================
# TELA LEGENDA
# =========================
class TelaLegenda(QWidget, BaseTela):
    def __init__(self):
        super().__init__()
        self.carregar_ui("tela/legenda.ui")

        self.carregar()

    def carregar(self):
        try:
            dados = carregar_legenda()

            if hasattr(self, "texto_legenda"):
                self.texto_legenda.setText(str(dados))

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar legenda: {e}")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    janela = TelaPrincipal()
    janela.show()

    sys.exit(app.exec_())