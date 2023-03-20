from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QSizePolicy, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from back import getCluster
import datePicker
import sys
import seaborn as sns


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

        self.comboBoxc = QComboBox(self)
        self.comboBoxc.addItems(['2', '3', '4', '5', '6', '7', '8', '9', '10'])
        self.comboBoxc.currentTextChanged.connect(self.drawChart)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(['Aoti', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
                                 'Gucheng', 'Huairou', 'Nongzhan', 'Shunyi', 'Tiantan',
                                 'Wanliu', 'Wanshouxigong'])
        self.comboBox2.currentTextChanged.connect(self.drawChart)
        self.start = datePicker.Datepicker(self, True)
        self.end = datePicker.Datepicker(self, False)
        self.start.setFixedHeight(120)
        self.end.setFixedHeight(120)

        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layoutv = QVBoxLayout()
        layoutv.addWidget(self.comboBoxa1)
        layoutv.addWidget(self.comboBoxa2)

        layoutv2 = QVBoxLayout()
        layoutv2.addWidget(self.comboBoxc)
        layoutv2.addWidget(self.comboBox2)

        layouth = QHBoxLayout()
        layouth.addLayout(layoutv)
        layouth.addLayout(layoutv2)
        layouth.addWidget(self.start)
        layouth.addWidget(self.end)

        layout = QVBoxLayout(self)
        layout.addLayout(layouth)
        layout.addWidget(self.canvas)

        self.setGeometry(300, 300, 1000, 700)
        self.show()
        self.drawChart()

    def drawChart(self):
        data, date, color = getCluster(self.comboBoxa1.currentText(), self.comboBoxa2.currentText(),
                                       str(self.comboBox2.currentIndex() + 1), self.start.select,
                                       self.end.select, self.comboBoxc.currentIndex() + 2)
        # cmap = sns.color_palette('bright', n_colors=10)
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)

        ax.scatter(range(len(data)), data, c=color, cmap="Paired", s=100, alpha=0.5)
        ax.set_title("with" + self.comboBoxa2.currentText())
        ax.set_xlabel("time")
        ax.set_ylabel(self.comboBoxa1.currentText())
        ax.set_xticklabels(date, rotation=15)
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PlotWidget()
    sys.exit(app.exec())
