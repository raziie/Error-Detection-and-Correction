import math
from itertools import repeat


# extended Hamming(15, 11)
# total bits = 15
# data = 11
# parity = 4
def generate_code(msg):
    code = [0] * 16
    parity_indexes = [0, 1, 2, 4, 8]
    msg_index = 0
    # make the message size 11
    # the whole message may not be dividable by 11
    if len(msg) < 11:
        msg = add_padding_zero(msg, 11 - len(msg))

    # add data to non_parity positions
    for i in range(len(code)):
        if i not in parity_indexes:
            code[i] = int(msg[msg_index])
            msg_index += 1

    # compute parities
    for i in parity_indexes[1:]:
        total = 0
        for j in range(len(code)):
            # convert j to 4-bit binary
            binary_index = bin(j)[2:].zfill(4)
            log_index = int(math.log2(i))
            # parity bit for indexes that their log_index is 1
            if binary_index[3 - log_index] == "1":
                total += code[j]
        code[i] = total % 2
    # parity of for bits
    code[0] = sum(code) % 2
    # convert to string
    return "".join([str(bit) for bit in code])


def is_power_two(n):
    return ((n & (n-1) == 0) and n != 0) or n == 0


def add_padding_zero(data, count):
    return data + "".join(list(repeat("0", count)))
