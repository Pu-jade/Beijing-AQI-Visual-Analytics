import sys
from PyQt6.QtCore import QDate, pyqtSignal
from PyQt6.QtWidgets import QApplication, QWidget, QCalendarWidget, QLabel, QVBoxLayout, QPushButton, QDialog


class DatePickerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.calendar = QCalendarWidget(self)
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(2013, 3, 1))
        self.calendar.setMaximumDate(QDate(2017, 2, 28))
        self.calendar.clicked.connect(self.accept)

        vbox = QVBoxLayout()
        vbox.addWidget(self.calendar)

        self.setLayout(vbox)

    def accept(self):
        date = self.calendar.selectedDate()
        self.parent().select = date.toString()
        self.parent().parent().drawChart()
        self.hide()


class Datepicker(QWidget):
    def __init__(self, parent=None, startOrEnd=True):
        super().__init__(parent)
        self.resize(100, 40)
        if startOrEnd:
            self.select = QDate(2013, 3, 1).toString()
            self.word = "Start Date: "
        else:
            self.select = QDate(2017, 2, 28).toString()
            self.word = "End Date: "

        self.label = QLabel(self)
        self.label.setText(self.word + self.select)

        self.dialog = DatePickerDialog(self)

        self.button = QPushButton("Select Date", self)
        self.button.clicked.connect(self.show_calendar)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.button)

        self.setLayout(vbox)

    def show_calendar(self):
        self.dialog = DatePickerDialog(self)
        result = self.dialog.exec()
        self.label.setText(self.word + self.select)
        # print(self.select)

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     datepicker = Datepicker(startOrEnd=False)
#     datepicker.show()
#     sys.exit(app.exec())
