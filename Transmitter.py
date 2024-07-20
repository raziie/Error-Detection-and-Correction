import socket
import time

import CRC
import HammingCode
import Parity
import Checksum


class Transmitter:

    def __init__(self, scroll_area, msg_label, progress_bar):
        # error detection and correction method
        self.method = None
        self.msg = ""
        self.data_size = 0

        # socket
        self.sock = None
        # GUI
        self.scroll_area = scroll_area
        self.msg_label = msg_label
        self.progress_bar = progress_bar

    def set_initial_data(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', 8080))
        self.data_size = 11 if self.method == 5 else 8
        self.start_sending()

    def start_sending(self):
        print('Ready\n\033[0;34m--------------- sender ---------------\u001b[0m')
        print('\033[1;33m >\u001b[0m message:{}'.format(self.msg))
        self.sock.settimeout(1)

        percent = int(800 / len(self.msg))

        # send data byte by byte
        # or 11 bit for hamming code
        for i in range(0, len(self.msg), self.data_size):
            # divide message into 8 bit chunks (11 for hamming code)
            msg_byte = self.msg[i:i + self.data_size]
            # add check bits to the end of message
            code = self.get_check_bits(msg_byte)
            self.send_msg(msg_byte, code)
            time.sleep(1)
            # update progress bar
            self.progress_bar.setProperty("value", self.progress_bar.value() + percent)

        # for 2D parity and checksum
        self.send_check_bits()
        # end of transmission
        self.sock.send('DISC'.encode())
        self.progress_bar.setProperty("value", 100)
        print('\033[1;33m >\u001b[0m sent message:\u001b[34m DISC\u001b[0m')
        self.sock.close()

    def send_msg(self, msg_byte, code):
        # for hamming code, code bits are between data bits
        if self.method == 5:
            print('\033[1;33m >\u001b[0m sent message:\033[0;32m{}\u001b[0m'.format(code))
            msg_coded = code
            self.scroll_area.append(">> " + code)
        else:
            print('\033[1;33m >\u001b[0m sent message:{}\033[0;32m{}\u001b[0m'.format(msg_byte, code))
            msg_coded = msg_byte + code
            self.scroll_area.append(">> " + msg_coded)
        self.sock.send(msg_coded.encode())

    def get_check_bits(self, msg):
        code = ""
        # parity and 2D parity
        if self.method == 1 or self.method == 2:
            code = str(Parity.compute_parity(msg))
        # CRC
        elif self.method == 4:
            code = CRC.generate_code(msg)
        # Hamming code
        elif self.method == 5:
            code = HammingCode.generate_code(msg)
        return code

    def send_check_bits(self):
        # 2D parity
        if self.method == 2:
            # convert the message to an array of bytes
            message_arr = [self.msg[i:i + self.data_size] for i in range(0, len(self.msg), self.data_size)]
            code = Parity.compute_column_parity(message_arr)
            self.send_msg("", code)
        # checksum
        elif self.method == 3:
            # convert the message to an array of bytes
            message_arr = [self.msg[i:i + self.data_size] for i in range(0, len(self.msg), self.data_size)]
            code = Checksum.compute_sum(message_arr)
            self.send_msg("", code)
