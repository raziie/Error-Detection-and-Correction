import socket
import time

import numpy

import Checksum
import Parity
import CRC


# Function to find the
# XOR of the two Binary Strings
def xor(a, b, n):
    return "".join(["0" if a[i] == b[i] else "1" for i in range(n)])


def generate_error(length):
    # create a random sequence of 0 and 1 with specified length
    # the probability of 0 is more
    return "".join(numpy.random.choice(numpy.arange(0, 2), p=[0.95, 0.05], size=length).astype(str))


class Receiver:

    def __init__(self, scroll_area, msg_label, error_field):
        # error detection and correction method
        self.method = 0
        self.msg_received = None
        self.data_size = 0
        self.error_pattern = []

        # socket part
        # socket.SOCK_STREAM => TCP : more reliable and maintain order of the msg and socket.AF_INET => ipv4
        self.sock = None
        self.conn = None

        # GUI
        self.error_format = '<span style="color:red;">{}</span>'
        self.correct_format = '<span style="color:green;">{}</span>'
        self.scroll_area = scroll_area
        self.msg_label = msg_label
        self.error_field = error_field

    def initiate_channel(self):
        self.error_pattern = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', 8080))
        self.sock.listen()
        print('listening')
        self.conn, addr = self.sock.accept()
        # get 11 bit packets for hamming code
        # and 8 bit for others
        self.data_size = 11 if self.method == 5 else 8
        # starts receiving
        self.receive()

    def receive(self):
        print('\033[0;34m--------------- receiver ---------------\u001b[0m\n', end='')
        data, without_correction = [], []
        byte, code = '', ''
        while True:
            byte = self.conn.recv(1024).decode()
            # DISC is a sign for end of transmission
            if byte == "DISC":
                print('\033[1;33m >\u001b[0m received message:\u001b[34m DISC\u001b[0m')
                break

            # received_data = data xor error
            error = generate_error(len(byte))
            byte = xor(byte, error, len(byte))
            self.error_pattern.append(error)

            if self.method == 5:
                print('\033[1;33m >\u001b[0m received message:\033[0;32m{}\u001b[0m'.format(byte))
                # add received data to GUI
                self.scroll_area.append(">> " + byte)
                # only hamming code can correct errors
                without_correction.append(byte)
                byte = self.detect_and_correct_errors(byte)
            else:
                # extract check bits
                code = byte[self.data_size:]
                byte = byte[0:self.data_size]
                print('\033[1;33m >\u001b[0m received message:{}\033[0;32m{}\u001b[0m'.format(byte, code))
                # add received data to GUI
                self.scroll_area.append(">> " + byte + code)
                self.detect_error(byte, code)

            data.append(byte)

        # getting check bits (for 2D parity and checksum)
        if self.method == 2 or self.method == 3:
            code = data[-1] + code
            data = data[:-1]
            self.detect_total_error(code, data)

        self.print_received_message(data, without_correction)
        self.print_error_pattern()

        time.sleep(2)
        self.conn.close()
        self.sock.close()

    def detect_error(self, byte, code):
        # parity or 2D parity
        if self.method == 1 or self.method == 2:
            parity = Parity.compute_parity(byte)
            # if the computed parity is different from the one that was sent
            # => error in odd number of bits
            # otherwise => no error or not detectable error (even number of bits)
            if parity != int(code):
                print("\033[0;31m error detected \u001b[0m")
                # add error msg to GUI
                self.scroll_area.append(">> error")
                # self.scroll_area.append(self.error_format.format(">> error"))
        # CRC
        elif self.method == 4:
            # pre_determined divisor
            p = "10011"
            remain = CRC.divide_modulo_two(byte + code, p)
            # if the division had no remainder then there is no error (probably)
            # or the error is dividable by p
            if remain != "0":
                print("\033[0;31m error detected \u001b[0m")
                # add error msg to GUI
                self.scroll_area.append(">> error")
                # self.scroll_area.append(self.error_format.format(">> error"))

    def detect_total_error(self, code, data):
        # 2D parity
        if self.method == 2:
            new_code = Parity.compute_column_parity(data)
            # if computed parity_seq is not equal to the one that is sent
            # => error detected (odd number of bits)
            # otherwise => no error or not detectable error (even number of bits)
            if code != new_code:
                # find differences in parity_seqs => error columns
                eor = xor(code, new_code, self.data_size)
                # find all occurrences of 1
                error_columns = [i for i in range(len(eor)) if eor[i] == "1"]
                print("\033[0;31m error detected at columns: ", error_columns, "\u001b[0m")
                # add error columns msg to GUI
                self.scroll_area.append(">> error columns: " + str(error_columns))
                # self.scroll_area.append(self.error_format.format(">> error columns: " + str(error_columns)))

        # checksum
        elif self.method == 3:
            received = data.copy()
            received.append(code)
            summation = Checksum.compute_sum(received)
            # sum of received data sequences and code should be 0
            # if not error detected
            # otherwise => no error or not detectable
            if int(summation, 2) != int("0", 2):
                print("\033[0;31m error detected \u001b[0m")
                # add error msg to GUI
                self.scroll_area.append(">> error")
                # self.scroll_area.append(self.error_format.format(">> error"))

    def detect_and_correct_errors(self, code):
        # Find all indices of '1'
        indices = [index for index in range(len(code)) if code.startswith('1', index)]
        # xor all positions (in binary) with value 1
        summation = "0000"
        for index in indices:
            summation = xor(summation, '{0:04b}'.format(index), 4)
        # if the final result is not zero => error detected at that index
        if summation != "0000":
            error_index = int(summation, 2)
            print("\033[0;31m error detected at index {}\u001b[0m".format(error_index))
            # add error at to GUI
            self.scroll_area.append(">> error at " + str(error_index) + "")
            # self.scroll_area.append(self.error_format.format(">> error at " + str(error_index) + ""))

            # more than 1 error (can't correct 2 bit error)
            if len(indices) % 2 == 0:
                print("\033[0;31m probably more than one bit, can't correct \u001b[0m")
                # add correct msg to GUI
                self.scroll_area.append(">> can't correct")
                # self.scroll_area.append(self.error_format.format(">> can't correct"))
            else:
                # correct the error
                # flip bit at error_index
                code = list(code)
                code[error_index] = "1" if code[error_index] == "0" else "0"
                code = "".join(code)
                print("\033[0;31m corrected it\033[0;32m ✓ \u001b[0m")
                # add correct msg to GUI
                self.scroll_area.append(">> corrected")
                # self.scroll_area.append(self.correct_format.format(">> corrected"))

        return code

    def extract_data(self, data_seq):
        new_data_seq = []
        parity_indexes = [0, 1, 2, 4, 8]
        # remove parity bits
        extracted = ""
        for data in data_seq:
            for i in range(len(data)):
                if i not in parity_indexes:
                    extracted += data[i]
        # convert to byte
        for i in range(0, len(extracted), 8):
            # ignore the last bits(they are zeros)
            # this happens because the input is dividable by 8 but not always by 11
            if len(extracted[i:i + 8]) < 8:
                break
            new_data_seq.append(extracted[i:i+8])

        return new_data_seq

    def print_error_pattern(self):
        # error pattern
        # print 1s (error bits) in red
        # also add error bits to GUI at the same time
        print("\nerror pattern: ")
        error_str = "\n".join(self.error_pattern)
        self.error_field.append(error_str)

        for error in self.error_pattern:
            # Find all indices of '1'
            indices = [index for index in range(len(error)) if error.startswith('1', index)]
            for i in range(len(error)):
                if i in indices:
                    print("\033[0;31m", error[i], "\u001b[0m", end='', sep='')
                    # self.error_field.insertPlainText(error[i])
                else:
                    print(error[i], end='')
                    # self.error_field.insertPlainText(error[i])
            print()
            # self.error_field.moveCursor(QTextCursor.End)
            # self.error_field.append("\n")

    def print_received_message(self, data, without_correction):
        # extract data from code (Hamming code)
        # also add msg to GUI
        if self.method == 5:
            data = self.extract_data(data)
            without_correction = self.extract_data(without_correction)
            without_correction = ''.join([chr(int(i, 2)) for i in without_correction])
            print('\n\033[1;33m >\u001b[0m without correction:' + without_correction)
            self.msg_label.setText("No correction = {}".format(without_correction))

        # change binary data that is received to ascii chars
        self.msg_received = ''.join([chr(int(i, 2)) for i in data])
        print('\n\033[1;33m >\u001b[0m received message:' + self.msg_received)
        self.msg_label.setText(self.msg_label.text() + "\nReceived msg = {}".format(self.msg_received))
