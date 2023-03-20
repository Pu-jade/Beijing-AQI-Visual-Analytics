from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

import current
import hist
import histpro
import corelate
import co3d
import Polar
import cluster


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(1000, 750)
        # 创建

        self.nonProView()


    def creat(self):
        self.current = current.Clock(self)


    def proView(self):
        self.resize(2500, 1800)
        self.creat()
        self.plotWidget = histpro.PlotWidget(self)
        self.plotWidget2 = corelate.PlotWidget(self)
        self.plotWidget3 = co3d.PlotWidget(self)
        self.plotWidget4 = Polar.PlotWidget(self)
        self.plotWidget5 = cluster.PlotWidget(self)

        self.button2 = QPushButton("Overview", self)
        self.button2.clicked.connect(self.nonProView)
        layouth = QHBoxLayout()
        layouth.addWidget(self.current)
        layouth.addWidget(self.plotWidget4)

        layouth2 = QHBoxLayout()
        layouth2.addWidget(self.plotWidget)
        layouth2.addWidget(self.plotWidget5)

        layouth3 = QHBoxLayout()
        layouth3.addWidget(self.plotWidget2)
        layouth3.addWidget(self.plotWidget3)

        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.button2)
        layout.addLayout(layouth)
        layout.addLayout(layouth2)
        layout.addLayout(layouth3)
        self.setCentralWidget(centralWidget)

    def nonProView(self):
        self.resize(1000, 1800)
        self.creat()
        self.plotWidget = hist.PlotWidget(self)
        self.plotWidget3 = corelate.PlotWidget(self)
        self.button = QPushButton("Pro", self)
        self.button.clicked.connect(self.proView)
        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        layout.addWidget(self.button)
        layout.addWidget(self.current)
        layout.addWidget(self.plotWidget)
        layout.addWidget(self.plotWidget3)
        self.setCentralWidget(centralWidget)


if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()