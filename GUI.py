import sys
from threading import Thread
import faulthandler

from PyQt5 import QtCore, QtGui, QtWidgets

from Receiver import Receiver
from Transmitter import Transmitter


class UiMainWindow(object):
    def setup(self, main_window):

        self.transmitter_thread = None
        self.receiver_thread = None

        self.main_window = main_window

        main_window.setObjectName("MainWindow")
        main_window.resize(1072, 856)

        # set the font
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semibold")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        main_window.setFont(font)

        main_window.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        main_window.setMouseTracking(False)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        # the place to enter message
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(380, 70, 201, 41))
        self.textEdit.setMinimumSize(QtCore.QSize(100, 30))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setPlaceholderText("Message")

        # send button
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(580, 70, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.send)

        # first laptop icon
        self.laptop1 = QtWidgets.QLabel(self.centralwidget)
        self.laptop1.setGeometry(QtCore.QRect(120, 140, 101, 101))
        self.laptop1.setText("")
        self.laptop1.setTextFormat(QtCore.Qt.AutoText)
        self.laptop1.setPixmap(QtGui.QPixmap("laptop.png"))
        self.laptop1.setScaledContents(True)
        self.laptop1.setObjectName("laptop1")

        # second laptop icon
        self.laptop2 = QtWidgets.QLabel(self.centralwidget)
        self.laptop2.setGeometry(QtCore.QRect(840, 140, 101, 101))
        self.laptop2.setText("")
        self.laptop2.setTextFormat(QtCore.Qt.AutoText)
        self.laptop2.setPixmap(QtGui.QPixmap("laptop.png"))
        self.laptop2.setScaledContents(True)
        self.laptop2.setObjectName("laptop2")

        # Transmitter label
        self.transmitter_label = QtWidgets.QLabel(self.centralwidget)
        self.transmitter_label.setGeometry(QtCore.QRect(120, 240, 120, 21))
        self.transmitter_label.setObjectName("transmitter_label")

        # Receiver label
        self.receiver_label = QtWidgets.QLabel(self.centralwidget)
        self.receiver_label.setGeometry(QtCore.QRect(850, 240, 120, 21))
        self.receiver_label.setObjectName("receiver_label")

        # error pattern label
        self.error_label = QtWidgets.QLabel(self.centralwidget)
        self.error_label.setGeometry(QtCore.QRect(460, 240, 150, 21))
        self.error_label.setStyleSheet("color: rgb(255, 0, 0);\n""font: 75 14pt \"Corbel\";\n""font-weight: bold;")
        self.error_label.setTextFormat(QtCore.Qt.PlainText)
        self.error_label.setObjectName("error_label")

        # set the font
        font2 = QtGui.QFont()
        font2.setFamily("Yu Gothic UI Semibold")
        font2.setPointSize(10)
        font2.setWeight(75)

        # sent msg
        self.sent_label = QtWidgets.QLabel(self.centralwidget)
        self.sent_label.setGeometry(QtCore.QRect(40, 680, 261, 100))
        self.sent_label.setObjectName("sent_label")
        self.sent_label.setFont(font2)

        # received msg
        self.received_label = QtWidgets.QLabel(self.centralwidget)
        self.received_label.setGeometry(QtCore.QRect(770, 680, 261, 100))
        self.received_label.setObjectName("received_label")
        self.received_label.setFont(font2)

        # transmitted bytes
        self.transmitted_bytes = QtWidgets.QTextEdit(self.centralwidget)
        self.transmitted_bytes.setGeometry(QtCore.QRect(40, 280, 261, 411))
        self.transmitted_bytes.setObjectName("transmitted_bytes")
        self.transmitted_bytes.setReadOnly(True)

        # received bytes
        self.received_bytes = QtWidgets.QTextEdit(self.centralwidget)
        self.received_bytes.setGeometry(QtCore.QRect(770, 280, 261, 411))
        self.received_bytes.setObjectName("received_bytes")
        self.received_bytes.setReadOnly(True)

        # error pattern
        self.error_pattern = QtWidgets.QTextEdit(self.centralwidget)
        self.error_pattern.setGeometry(QtCore.QRect(400, 280, 261, 411))
        self.error_pattern.setObjectName("error_pattern")
        self.error_pattern.setReadOnly(True)

        # progress bar
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(340, 180, 371, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1072, 30))
        self.menubar.setObjectName("menubar")

        self.menuMethod = QtWidgets.QMenu(self.menubar)
        self.menuMethod.setObjectName("menuMethod")

        self.menuExit = QtWidgets.QAction(self.menubar)
        self.menuExit.setObjectName("menuExit")
        main_window.setMenuBar(self.menubar)
        self.menuExit.triggered.connect(self.exit)

        # initial sender and receiver
        self.receiver = Receiver(self.received_bytes, self.received_label, self.error_pattern)
        self.transmitter = Transmitter(self.transmitted_bytes, self.sent_label, self.progressBar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setStatusTip("")
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.action1_simple_parity_check = QtWidgets.QAction(main_window)
        self.action1_simple_parity_check.setObjectName("action1_simple_parity_check")

        self.action2D_parity_check = QtWidgets.QAction(main_window)
        self.action2D_parity_check.setObjectName("action2D_parity_check")

        self.action_checksum = QtWidgets.QAction(main_window)
        self.action_checksum.setObjectName("action_checksum")

        self.action_cycle_redundancy_check_CRC = QtWidgets.QAction(main_window)
        self.action_cycle_redundancy_check_CRC.setObjectName("action_cycle_redundancy_check_CRC")

        self.action_hamming_code = QtWidgets.QAction(main_window)
        self.action_hamming_code.setObjectName("action_hamming_code")

        self.set_menu_methods()

        self.menuMethod.addAction(self.action1_simple_parity_check)
        self.menuMethod.addSeparator()
        self.menuMethod.addAction(self.action2D_parity_check)
        self.menuMethod.addSeparator()
        self.menuMethod.addAction(self.action_checksum)
        self.menuMethod.addSeparator()
        self.menuMethod.addAction(self.action_cycle_redundancy_check_CRC)
        self.menuMethod.addSeparator()
        self.menuMethod.addAction(self.action_hamming_code)
        self.menubar.addAction(self.menuMethod.menuAction())
        self.menubar.addAction(self.menuExit)

        self.retranslateUi(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Error Detection & Correction"))
        self.pushButton.setText(_translate("MainWindow", "Send"))
        self.transmitter_label.setText(_translate("MainWindow", "Transmitter"))
        self.receiver_label.setText(_translate("MainWindow", "Receiver"))
        self.error_label.setText(_translate("MainWindow", "Error pattern"))
        self.menuMethod.setTitle(_translate("MainWindow", "Method"))
        self.menuExit.setText(_translate("MainWindow", "Exit"))
        self.action1_simple_parity_check.setText(_translate("MainWindow", "simple parity check"))
        self.action2D_parity_check.setText(_translate("MainWindow", "2D parity check"))
        self.action_checksum.setText(_translate("MainWindow", "checksum"))
        self.action_cycle_redundancy_check_CRC.setText(_translate("MainWindow", "cycle redundancy check (CRC)"))
        self.action_hamming_code.setText(_translate("MainWindow", "Hamming code"))

    def send(self):
        # if self.transmitter_thread:
        #     self.transmitter_thread.join()
        # if self.receiver_thread:
        #     self.receiver_thread.join()

        # reset everything
        self.transmitted_bytes.setText("")
        self.received_bytes.setText("")
        self.error_pattern.setText("")
        self.progressBar.setProperty("value", 0)
        self.sent_label.setText("")
        self.received_label.setText("")

        message = self.textEdit.toPlainText()
        print("message to send is => \"{}\"".format(message))
        self.sent_label.setText("Sent msg = {}".format(message))
        # using join() + ord() + format()
        # Converting String to binary
        binary_message = str(''.join(format(ord(i), '08b') for i in message))
        self.transmitter.msg = binary_message

        self.transmitter_thread = Thread(target=self.receiver.initiate_channel)
        self.receiver_thread = Thread(target=self.transmitter.set_initial_data)

        self.receiver_thread.start()
        self.transmitter_thread.start()

    def set_menu_methods(self):
        self.action1_simple_parity_check.triggered.connect(lambda: self.set_method(1))
        self.action2D_parity_check.triggered.connect(lambda: self.set_method(2))
        self.action_checksum.triggered.connect(lambda: self.set_method(3))
        self.action_cycle_redundancy_check_CRC.triggered.connect(lambda: self.set_method(4))
        self.action_hamming_code.triggered.connect(lambda: self.set_method(5))

    def set_method(self, method_num):
        self.receiver.method = method_num
        self.transmitter.method = method_num
        print("setting the method to", method_num)

        title = ""
        if method_num == 1:
            title = "simple parity check"
        elif method_num == 2:
            title = "2D parity check"
        elif method_num == 3:
            title = "checksum"
        elif method_num == 4:
            title = "CRC"
        else:
            title = "Hamming code"

        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", title))

    def exit(self):
        # closing the window
        self.main_window.close()


if __name__ == "__main__":
    faulthandler.enable()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup(MainWindow)
    MainWindow.show()
    print("I'm exiting")
    sys.exit(app.exec_())
