import sys
import mysql.connector
import conexao
print(dir(conexao))

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QCalendarWidget, QLabel, QTextEdit, QPushButton
)
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QTextCharFormat, QColor


class CalendarioApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("tela/calendario.ui")

      
        self.conn = conexao.conectar()
        self.cursor = self.conn.cursor()

        layout = QVBoxLayout()

        self.calendario = QCalendarWidget()
        self.calendario.clicked.connect(self.data_selecionada)

       

        layout.addWidget(self.calendario)

        self.setLayout(layout)

        # carregar marcações
        self.atualizar_formatacao()

    # 📅 quando clica na data
    def data_selecionada(self, data: QDate):
        ano, mes, dia = data.year(), data.month(), data.day()

        self.label_data.setText(f"{dia}/{mes}/{ano}")

        self.cursor.execute(
            "SELECT * FROM legendas WHERE ano=%s AND mes=%s AND dia=%s",
            (ano, mes, dia)
        )

        resultado = self.cursor.fetchone()

        if resultado:
            self.texto_evento.setText(resultado[0])
        else:
            self.texto_evento.clear()

    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CalendarioApp()
    janela.resize(800, 600)
    janela.show()
    sys.exit(app.exec_())