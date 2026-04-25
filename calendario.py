import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QCalendarWidget, QLabel, QTextEdit, QPushButton, QComboBox
)
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtCore import QDate

import conexao


class CalendarioApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calendário Profissional")
        self.resize(1000, 600)

        self.conn = conexao.conectar()
        self.cursor = self.conn.cursor()

        layout_principal = QHBoxLayout()

        # 📅 CALENDÁRIO
        self.calendario = QCalendarWidget()
        self.calendario.clicked.connect(self.data_selecionada)

        layout_principal.addWidget(self.calendario)

        # 📌 LADO DIREITO
        layout_direita = QVBoxLayout()

        self.label_data = QLabel("Selecione uma data")

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            "FERIADO",
            "RECESSO",
            "PLANEJAMENTO",
            "INICIO_CURSO",
            "AULA",
            "CAPACITACAO",
            "REUNIAO",
            "ESTAGIO",
            "FIM_CURSO"
        ])

        self.texto_evento = QTextEdit()

        self.btn_salvar = QPushButton("Salvar Evento")
        self.btn_salvar.clicked.connect(self.salvar_evento)

        layout_direita.addWidget(self.label_data)
        layout_direita.addWidget(self.combo_tipo)
        layout_direita.addWidget(self.texto_evento)
        layout_direita.addWidget(self.btn_salvar)

        # 🎨 LEGENDA
        layout_direita.addWidget(QLabel("Legenda:"))

        self.legenda = {
            "FERIADO": "red",
            "RECESSO": "blue",
            "PLANEJAMENTO": "orange",
            "INICIO_CURSO": "green",
            "AULA": "purple",
            "CAPACITACAO": "pink",
            "REUNIAO": "cyan",
            "ESTAGIO": "brown",
            "FIM_CURSO": "black"
        }

        for nome, cor in self.legenda.items():
            lbl = QLabel(nome)
            lbl.setStyleSheet(f"color: {cor}; font-weight: bold;")
            layout_direita.addWidget(lbl)

        layout_principal.addLayout(layout_direita)

        self.setLayout(layout_principal)

        self.atualizar_formatacao()

    # 📅 clicar na data
    def data_selecionada(self, data: QDate):
        self.data_atual = data

        ano, mes, dia = data.year(), data.month(), data.day()
        self.label_data.setText(f"{dia}/{mes}/{ano}")

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

    # 💾 salvar
    def salvar_evento(self):
        if not hasattr(self, "data_atual"):
            return

        data = self.data_atual
        ano, mes, dia = data.year(), data.month(), data.day()
        tipo = self.combo_tipo.currentText()
        texto = self.texto_evento.toPlainText()

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
        self.atualizar_formatacao()

    # 🎨 pintar dias
    def atualizar_formatacao(self):
        self.calendario.setDateTextFormat(QDate(), QTextCharFormat())

        self.cursor.execute("SELECT ano, mes, dia, tipo FROM legendas")
        eventos = self.cursor.fetchall()

        for ano, mes, dia, tipo in eventos:
            data = QDate(ano, mes, dia)

            formato = QTextCharFormat()
            cor = self.legenda.get(tipo, "gray")
            formato.setBackground(QColor(cor))

            self.calendario.setDateTextFormat(data, formato)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CalendarioApp()
    janela.show()
    sys.exit(app.exec_())