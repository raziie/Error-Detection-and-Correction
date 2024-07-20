from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    # this function will be called when the button is pressed
    def clicked(self):
        self.label.setText("pressed!!!!!!!!!!!!!!!!!!!!!")
        # to adjust size
        self.label.adjustSize()

    def initUI(self):
        # set size (aw, ah)
        self.resize(1000, 500)
        # set title
        self.setWindowTitle("Error Detection & Correction")

        # TODO: change it from here
        # add label
        self.label = QLabel(self)
        self.label.setText("my first label")
        self.label.move(50, 50)

        # add button
        self.button = QtWidgets.QPushButton(self)
        self.button.setText("click")
        self.button.clicked.connect(self.clicked)  # no brackets for function (we are not calling it)
        self.button.move(200, 200)


def main():
    # where we can place our window and widgets
    app = QApplication(sys.argv)
    # a container that will hold all of our widgets (buttons, labels, etc.)
    window = Window()

    window.show()
    sys.exit(app.exec_())


main()
