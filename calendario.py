from PyQt5 import uic, QtWidgets, QtCore, QtGui
import conexao
import os


class CalendarioApp(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.join(
                os.path.dirname(__file__),
                "tela",
                "calendario.ui"
            ),
            self
        )

        self.conn = None
        self.cursor = None
        self.data_atual = None

        try:

            self.conn = conexao.conectar()
            self.cursor = self.conn.cursor()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro de conexão",
                str(e)
            )

        if hasattr(self, "calendarWidget"):
            self.calendarWidget.clicked.connect(
                self.data_selecionada
            )

        if hasattr(self, "combo_tipo"):

            self.combo_tipo.clear()

            self.combo_tipo.addItems(
                sorted(self.legenda.keys())
            )

        else:

            self.criar_controles_calendario_fallback()

        self.atualizar_formatacao()

    @property
    def legenda(self):

        return {
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
            "TREINAMENTO": "darkgreen",
        }

    def criar_controles_calendario_fallback(self):

        self.combo_tipo = QtWidgets.QComboBox(self)
        self.combo_tipo.addItems(
            sorted(self.legenda.keys())
        )

        self.texto_evento = QtWidgets.QTextEdit(self)

        self.btn_salvar = QtWidgets.QPushButton(
            "Salvar evento",
            self
        )

        self.label_data = QtWidgets.QLabel(
            "Data: -",
            self
        )

        self.combo_tipo.setGeometry(
            20, 20, 240, 30
        )

        self.texto_evento.setGeometry(
            20, 60, 240, 120
        )

        self.btn_salvar.setGeometry(
            20, 190, 240, 35
        )

        self.label_data.setGeometry(
            20, 235, 240, 25
        )

        self.btn_salvar.clicked.connect(
            self.salvar_evento
        )

    def data_selecionada(self, data):

        self.data_atual = data

        if hasattr(self, "label_data"):

            self.label_data.setText(
                f"{data.day()}/{data.month()}/{data.year()}"
            )

        if (
            not self.cursor
            or not hasattr(self, "combo_tipo")
            or not hasattr(self, "texto_evento")
        ):
            return

        ano = data.year()
        mes = data.month()
        dia = data.day()

        try:

            self.cursor.execute(
                """
                SELECT tipo, texto
                FROM legendas
                WHERE ano=%s AND mes=%s AND dia=%s
                """,
                (ano, mes, dia)
            )

            resultado = self.cursor.fetchone()

            if resultado:

                self.combo_tipo.setCurrentText(
                    resultado[0]
                )

                self.texto_evento.setPlainText(
                    resultado[1]
                )

            else:

                self.texto_evento.clear()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def salvar_evento(self):

        if not self.data_atual:

            QtWidgets.QMessageBox.warning(
                self,
                "Aviso",
                "Selecione uma data primeiro!"
            )

            return

        if not self.cursor:

            QtWidgets.QMessageBox.warning(
                self,
                "Aviso",
                "Não foi possível acessar o banco de dados."
            )

            return

        ano = self.data_atual.year()
        mes = self.data_atual.month()
        dia = self.data_atual.day()

        tipo = self.combo_tipo.currentText()
        texto = self.texto_evento.toPlainText()

        try:

            self.cursor.execute(
                """
                SELECT id
                FROM legendas
                WHERE ano=%s AND mes=%s AND dia=%s
                """,
                (ano, mes, dia)
            )

            resultado = self.cursor.fetchone()

            if resultado:

                self.cursor.execute(
                    """
                    UPDATE legendas
                    SET tipo=%s, texto=%s
                    WHERE id=%s
                    """,
                    (
                        tipo,
                        texto,
                        resultado[0]
                    )
                )

            else:

                self.cursor.execute(
                    """
                    INSERT INTO legendas
                    (ano, mes, dia, tipo, texto)
                    VALUES (%s,%s,%s,%s,%s)
                    """,
                    (
                        ano,
                        mes,
                        dia,
                        tipo,
                        texto
                    )
                )

            self.conn.commit()

            self.atualizar_formatacao()

            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "Evento salvo com sucesso!"
            )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro ao salvar",
                str(e)
            )

    def atualizar_formatacao(self):

        if (
            not hasattr(self, "calendarWidget")
            or not self.cursor
        ):
            return

        try:

            self.calendarWidget.setDateTextFormat(
                QtCore.QDate(),
                QtGui.QTextCharFormat()
            )

            self.cursor.execute(
                """
                SELECT ano, mes, dia, tipo
                FROM legendas
                """
            )

            eventos = self.cursor.fetchall()

            for ano, mes, dia, tipo in eventos:

                data = QtCore.QDate(
                    ano,
                    mes,
                    dia
                )

                formato = QtGui.QTextCharFormat()

                cor = self.legenda.get(
                    tipo,
                    "gray"
                )

                formato.setBackground(
                    QtGui.QColor(cor)
                )

                self.calendarWidget.setDateTextFormat(
                    data,
                    formato
                )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def closeEvent(self, event):

        if self.conn:

            try:
                self.cursor.close()
                self.conn.close()
            except:
                pass

        event.accept()