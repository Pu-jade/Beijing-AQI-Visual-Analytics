import numpy as np
import pandas as pd
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QSizePolicy, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout
from PyQt6.QtCore import QObject, pyqtSignal
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from back import update_heatmap
import sys


class PlotWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd",
                                "WSPM"])
        self.comboBox.currentTextChanged.connect(self.update)

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(['Aoti', 'Changping', 'Dingling', 'Dongsi', 'Guanyuan',
                                 'Gucheng', 'Huairou', 'Nongzhan', 'Shunyi', 'Tiantan',
                                 'Wanliu', 'Wanshouxigong'])
        self.comboBox2.currentTextChanged.connect(self.update)

        self.label = QLabel()

        pixmap = QPixmap('polar.png')


        self.label.setPixmap(pixmap.scaled(300, 300))

        layouth = QHBoxLayout()
        layouth.addWidget(self.comboBox)
        layouth.addWidget(self.comboBox2)

        layout = QVBoxLayout(self)
        layout.addLayout(layouth)
        layout.addWidget(self.label)


        self.setGeometry(200, 200, 200, 200)
        self.show()

    def update(self):
        update_heatmap(self.comboBox.currentText(), self.comboBox2.currentIndex() + 1)
        pixmap = QPixmap('polar.png')
        self.label.setPixmap(pixmap.scaled(300, 300))


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = PlotWidget()
#     sys.exit(app.exec())
