from PyQt5 import QtWidgets


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