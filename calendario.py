import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
import conexao
import os


class CalendarioApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Carrega interface do Qt Designer
        uic.loadUi(os.path.join(os.path.dirname(__file__), "tela", "calendario.ui"), self)

        # Conexão com banco
        self.conn = conexao.conectar()
        self.cursor = self.conn.cursor()

        # data selecionada
        self.data_atual = None

        # conecta eventos da UI
        self.calendarWidget.clicked.connect(self.data_selecionada)
        self.btn_salvar.clicked.connect(self.salvar_evento)

        # legenda de cores
        self.legenda = {
            "FERIADO": "red",
            "RECESSO": "blue",
            "PLANEJAMENTO": "orange",
            "INICIO_CURSO": "green",
            "AULA": "purple",
            "CAPACITACAO": "pink",
            "REUNIAO": "cyan",
            "ESTAGIO": "brown",
            "FIM_CURSO": "black",
            "PROVA": "darkred",
            "AVALIACAO": "darkblue",
            "TREINAMENTO": "darkgreen"
        }

        # 🔥 CARREGA EVENTOS AO ABRIR
        self.atualizar_formatacao()

    # =========================
    # AO CLICAR NO DIA
    # =========================
    def data_selecionada(self, data: QtCore.QDate):
        self.data_atual = data

        ano, mes, dia = data.year(), data.month(), data.day()
        self.label_data.setText(f"{dia}/{mes}/{ano}")

        try:
            self.cursor.execute(
                "SELECT tipo, texto FROM legendas WHERE ano=%s AND mes=%s AND dia=%s",
                (ano, mes, dia)
            )

            resultado = self.cursor.fetchone()

            if resultado:
                self.combo_tipo.setCurrentText(resultado[0])
                self.texto_evento.setText(resultado[1])
            else:
                self.texto_evento.clear()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))

    # =========================
    # SALVAR EVENTO
    # =========================
    def salvar_evento(self):
        if not self.data_atual:
            QtWidgets.QMessageBox.warning(self, "Aviso", "Selecione uma data primeiro!")
            return

        ano = self.data_atual.year()
        mes = self.data_atual.month()
        dia = self.data_atual.day()

        tipo = self.combo_tipo.currentText()
        texto = self.texto_evento.toPlainText()

        try:
            # verifica se já existe
            self.cursor.execute(
                "SELECT id FROM legendas WHERE ano=%s AND mes=%s AND dia=%s",
                (ano, mes, dia)
            )

            resultado = self.cursor.fetchone()

            if resultado:
                self.cursor.execute(
                    "UPDATE legendas SET tipo=%s, texto=%s WHERE id=%s",
                    (tipo, texto, resultado[0])
                )
            else:
                self.cursor.execute(
                    "INSERT INTO legendas (ano, mes, dia, tipo, texto) VALUES (%s,%s,%s,%s,%s)",
                    (ano, mes, dia, tipo, texto)
                )

            self.conn.commit()

            # 🔥 atualiza calendário imediatamente
            self.atualizar_formatacao()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro ao salvar", str(e))

    # =========================
    # CARREGAR E PINTAR CALENDÁRIO
    # =========================
    def atualizar_formatacao(self):
        try:
            # limpa formatações antigas
            self.calendarWidget.setDateTextFormat(
                QtCore.QDate(),
                QtGui.QTextCharFormat()
            )

            self.cursor.execute("SELECT ano, mes, dia, tipo FROM legendas")
            eventos = self.cursor.fetchall()

            for ano, mes, dia, tipo in eventos:
                data = QtCore.QDate(ano, mes, dia)

                formato = QtGui.QTextCharFormat()
                cor = self.legenda.get(tipo, "gray")

                formato.setBackground(QtGui.QColor(cor))

                self.calendarWidget.setDateTextFormat(data, formato)

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Erro", str(e))


# =========================
# EXECUÇÃO ISOLADA (teste)
# =========================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    janela = CalendarioApp()
    janela.show()

    sys.exit(app.exec_())