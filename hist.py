from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QComboBox, QSizePolicy, QWidget, QVBoxLayout, \
    QLabel, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from back import getData
import sys

class PlotWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 创建一个下拉框
        self.comboBox = QComboBox(self)
        self.comboBox.move(50, 50)
        self.comboBox.addItems(["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "PRES", "DEWP", "RAIN", "wd", "WSPM"])
        self.comboBox.currentTextChanged.connect(self.drawChart)

        # 创建一个图形对象和一个画布对象
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.canvas)

        self.setGeometry(300, 300, 1000, 800)
        self.show()
        self.drawChart()

    def drawChart(self):
        # 清空之前的图形
        data, date = getData(self.comboBox.currentText())
        self.figure.clear()
        # 创建一个子图对象
        ax = self.figure.add_subplot(1, 1, 1)
        # 绘制折线图
        # print(data)
        ax.plot(data)
        ax.set_xlabel('time')
        ax.set_ylabel(self.comboBox.currentText())
        ax.set_xticklabels(date, rotation=15)
        # 更新画布
        self.canvas.draw()


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = PlotWidget()
#     sys.exit(app.exec())
