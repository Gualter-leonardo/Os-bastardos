from PyQt5 import uic, QtWidgets, QtCore, QtGui

from PyQt5.QtGui import QPixmap

import conexao
import os


class CalendarioMensal(QtWidgets.QCalendarWidget):

    def paintCell(self, painter, rect, date):

        if (
            date.year() != self.yearShown()
            or date.month() != self.monthShown()
        ):
            return

        super().paintCell(
            painter,
            rect,
            date
        )


class CalendarioApp(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        caminho = os.path.join(
            os.path.dirname(__file__),
            "tela",
            "calendario.ui"
        )

        uic.loadUi(
            caminho,
            self
        )

        self.conn = None
        self.cursor = None
        self.data_atual = None

        self.substituir_calendario()

        try:

            self.conn = conexao.conectar()

            self.cursor = self.conn.cursor()

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro de conexão",
                str(e)
            )

        if hasattr(
            self,
            "calendarWidget"
        ):

            self.calendarWidget.clicked.connect(
                self.data_selecionada
            )

            self.calendarWidget.currentPageChanged.connect(
                self.pagina_mudou
            )

        if hasattr(
            self,
            "combo_tipo"
        ):

            self.combo_tipo.clear()

            self.combo_tipo.addItems(
                sorted(
                    self.legenda.keys()
                )
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

            "TREINAMENTO": "darkgreen"
        }

    def substituir_calendario(self):

        if not hasattr(
            self,
            "calendarWidget"
        ):
            return

        calendario_antigo = self.calendarWidget

        calendario_novo = CalendarioMensal(
            calendario_antigo.parent()
        )

        calendario_novo.setObjectName(
            "calendarWidget"
        )

        calendario_novo.setGeometry(
            calendario_antigo.geometry()
        )

        calendario_novo.setLocale(
            calendario_antigo.locale()
        )

        calendario_novo.setFirstDayOfWeek(
            calendario_antigo.firstDayOfWeek()
        )

        calendario_novo.setGridVisible(
            calendario_antigo.isGridVisible()
        )

        calendario_novo.setVerticalHeaderFormat(
            calendario_antigo.verticalHeaderFormat()
        )

        calendario_novo.setHorizontalHeaderFormat(
            calendario_antigo.horizontalHeaderFormat()
        )

        calendario_novo.setNavigationBarVisible(
            calendario_antigo.isNavigationBarVisible()
        )

        calendario_novo.setSelectionMode(
            calendario_antigo.selectionMode()
        )

        calendario_novo.setMinimumDate(
            calendario_antigo.minimumDate()
        )

        calendario_novo.setMaximumDate(
            calendario_antigo.maximumDate()
        )

        calendario_novo.setSelectedDate(
            calendario_antigo.selectedDate()
        )

        layout = calendario_antigo.parentWidget().layout()

        if layout is not None:

            indice = layout.indexOf(
                calendario_antigo
            )

            if indice >= 0:

                layout.removeWidget(
                    calendario_antigo
                )

                calendario_antigo.setParent(
                    None
                )

                calendario_antigo.deleteLater()

                layout.insertWidget(
                    indice,
                    calendario_novo
                )

            else:

                calendario_antigo.hide()

        else:

            calendario_antigo.hide()

            calendario_novo.show()

        self.calendarWidget = calendario_novo

        self.calendarWidget.show()

    def pagina_mudou(
        self,
        ano,
        mes
    ):

        self.atualizar_formatacao()

    def criar_controles_calendario_fallback(self):

        self.combo_tipo = QtWidgets.QComboBox(
            self
        )

        self.combo_tipo.addItems(
            sorted(
                self.legenda.keys()
            )
        )

        self.texto_evento = QtWidgets.QTextEdit(
            self
        )

        self.btn_salvar = QtWidgets.QPushButton(
            "Salvar evento",
            self
        )

        self.label_data = QtWidgets.QLabel(
            "Data: -",
            self
        )

        self.combo_tipo.setGeometry(
            20,
            20,
            240,
            30
        )

        self.texto_evento.setGeometry(
            20,
            60,
            240,
            120
        )

        self.btn_salvar.setGeometry(
            20,
            190,
            240,
            35
        )

        self.label_data.setGeometry(
            20,
            235,
            240,
            25
        )

        self.btn_salvar.clicked.connect(
            self.salvar_evento
        )

    def data_selecionada(
        self,
        data
    ):

        self.data_atual = data

        if hasattr(
            self,
            "label_data"
        ):

            self.label_data.setText(
                f"{data.day()}/"
                f"{data.month()}/"
                f"{data.year()}"
            )

        if not self.cursor:
            return

        if not hasattr(
            self,
            "combo_tipo"
        ):
            return

        if not hasattr(
            self,
            "texto_evento"
        ):
            return

        try:

            sql = (
                "SELECT tipo, texto "
                "FROM legendas "
                "WHERE ano=%s "
                "AND mes=%s "
                "AND dia=%s"
            )

            self.cursor.execute(
                sql,
                (
                    data.year(),
                    data.month(),
                    data.day()
                )
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
                "Não foi possível conectar ao banco de dados."
            )

            return

        try:

            ano = self.data_atual.year()

            mes = self.data_atual.month()

            dia = self.data_atual.day()

            tipo = self.combo_tipo.currentText()

            texto = self.texto_evento.toPlainText()

            sql = (
                "SELECT id "
                "FROM legendas "
                "WHERE ano=%s "
                "AND mes=%s "
                "AND dia=%s"
            )

            self.cursor.execute(
                sql,
                (
                    ano,
                    mes,
                    dia
                )
            )

            resultado = self.cursor.fetchone()

            if resultado:

                sql = (
                    "UPDATE legendas "
                    "SET tipo=%s, texto=%s "
                    "WHERE id=%s"
                )

                self.cursor.execute(
                    sql,
                    (
                        tipo,
                        texto,
                        resultado[0]
                    )
                )

            else:

                sql = (
                    "INSERT INTO legendas "
                    "(ano, mes, dia, tipo, texto) "
                    "VALUES (%s, %s, %s, %s, %s)"
                )

                self.cursor.execute(
                    sql,
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
                "Evento salvo com sucesso."
            )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )

    def atualizar_formatacao(self):

        if not hasattr(
            self,
            "calendarWidget"
        ):
            return

        calendario = self.calendarWidget

        if not self.cursor:
            return

        try:

            ano_atual = calendario.yearShown()

            mes_atual = calendario.monthShown()

            sql = (
                "SELECT ano, mes, dia, tipo "
                "FROM legendas"
            )

            self.cursor.execute(
                sql
            )

            eventos = self.cursor.fetchall()

            for ano, mes, dia, tipo in eventos:

                if (
                    ano != ano_atual
                    or mes != mes_atual
                ):
                    continue

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

                formato.setForeground(
                    QtGui.QColor("white")
                )

                calendario.setDateTextFormat(
                    data,
                    formato
                )

        except Exception as e:

            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                str(e)
            )
        self.substituir_calendario()