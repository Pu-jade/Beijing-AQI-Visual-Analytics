import get
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QTimer, QTime


class Clock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(0, 0, 500, 100)
        self.setWindowTitle('Clock')

        self.label = QLabel(self)
        self.label.setGeometry(20, 0, 400, 40)
        self.label.setStyleSheet("font-size: 20px; font-weight: bold;")

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

        self.label2 = QLabel(self)
        self.label2.setGeometry(20, 50, 400, 100)
        self.label2.setStyleSheet("font-size: 30px; font-weight: bold;")

        self.update_aqi()
        timer2 = QTimer(self)
        timer2.timeout.connect(self.update_aqi)
        timer2.start(600000)

        self.show()

    def showTime(self):
        current_time = QTime.currentTime().toString('hh:mm')
        self.label.setText("Current time: " + current_time)

    def update_aqi(self):
        aqi, color = get.getCurrent()
        print(aqi)
        self.label2.setStyleSheet("font-size: 30px; font-weight: bold; color: " + color + ";")
        self.label2.setText("Current AQI: " + str(aqi) + "\n if other Data need")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     clock = Clock()
#     sys.exit(app.exec())
