from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QSizePolicy, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from back import getData
import datePicker
import sys


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd",
                                "WSPM"])
        self.comboBox.currentTextChanged.connect(self.drawChart)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(['Aoti', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
                                 'Gucheng', 'Huairou', 'Nongzhan', 'Shunyi', 'Tiantan',
                                 'Wanliu', 'Wanshouxigong'])
        self.comboBox2.currentTextChanged.connect(self.drawChart)
        self.start = datePicker.Datepicker(self, True)
        self.end = datePicker.Datepicker(self, False)
        self.start.setFixedHeight(90)
        self.end.setFixedHeight(90)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layoutv = QVBoxLayout()
        layoutv.addWidget(self.comboBox)
        layoutv.addWidget(self.comboBox2)

        layouth = QHBoxLayout()
        layouth.addLayout(layoutv)
        layouth.addWidget(self.start)
        layouth.addWidget(self.end)

        layout = QVBoxLayout(self)
        layout.addLayout(layouth)
        layout.addWidget(self.canvas)

        self.setGeometry(300, 300, 1000, 800)
        self.show()
        self.drawChart()

    def drawChart(self):
        data, date = getData(self.comboBox.currentText(), str(self.comboBox2.currentIndex() + 1),
                             self.start.select, self.end.select)
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.plot(data)
        ax.set_xlabel('time')
        ax.set_ylabel(self.comboBox.currentText())
        ax.set_xticklabels(date, rotation=15)
        self.canvas.draw()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = PlotWidget()
#     sys.exit(app.exec())
