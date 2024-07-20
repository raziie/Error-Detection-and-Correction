def compute_sum(total_msg):
    # compute sum of all bytes
    summation = "0"
    for byte in total_msg:
        summation = binary_sum(summation, byte)
    # adding the overflow bits
    summation = binary_sum(summation[len(summation) - 8:], summation[:len(summation) - 8])
    # one's complement sum
    return ones_complement(summation)


def binary_sum(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]


def ones_complement(byte):
    return "".join([flip(bit) for bit in byte])


def flip(bit):
    return '1' if (bit == '0') else '0'
