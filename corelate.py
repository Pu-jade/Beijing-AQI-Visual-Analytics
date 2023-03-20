from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QSizePolicy, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from back import getData
import datePicker
import sys


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.comboBoxa1 = QComboBox(self)
        self.comboBoxa1.addItems(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd",
                                  "WSPM"])
        self.comboBoxa1.currentTextChanged.connect(self.drawChart)

        self.comboBoxa2 = QComboBox(self)
        self.comboBoxa2.addItems(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd",
                                  "WSPM"])
        self.comboBoxa2.currentTextChanged.connect(self.drawChart)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(['Aoti', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
                                 'Gucheng', 'Huairou', 'Nongzhan', 'Shunyi', 'Tiantan',
                                 'Wanliu', 'Wanshouxigong'])
        self.comboBox2.currentTextChanged.connect(self.drawChart)
        self.start = datePicker.Datepicker(self, True)
        self.end = datePicker.Datepicker(self, False)
        self.start.setFixedHeight(120)
        self.end.setFixedHeight(120)

        # 创建一个图形对象和一个画布对象
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layoutv = QVBoxLayout()
        layoutv.addWidget(self.comboBoxa1)
        layoutv.addWidget(self.comboBoxa2)
        layoutv.addWidget(self.comboBox2)

        layouth = QHBoxLayout()
        layouth.addLayout(layoutv)
        layouth.addWidget(self.start)
        layouth.addWidget(self.end)

        layout = QVBoxLayout(self)
        layout.addLayout(layouth)
        layout.addWidget(self.canvas)

        self.setGeometry(300, 300, 1000, 700)
        self.show()
        self.drawChart()

    def drawChart(self):
        data1, _ = getData(self.comboBoxa1.currentText(), str(self.comboBox2.currentIndex() + 1),
                           self.start.select, self.end.select)
        data2, _ = getData(self.comboBoxa2.currentText(), str(self.comboBox2.currentIndex() + 1),
                           self.start.select, self.end.select)
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        ax.scatter(data1, data2)
        ax.set_xlabel(self.comboBoxa1.currentText())
        ax.set_ylabel(self.comboBoxa2.currentText())
        self.canvas.draw()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = PlotWidget()
#     sys.exit(app.exec())
