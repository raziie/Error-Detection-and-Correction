from itertools import repeat


def generate_code(msg):
    # p = x^4 + x + 1 = 10011
    # n-k+1 = 5
    # n-k = 4 = frame check sequence bits (FCS)
    # k = 8 (data)
    n = 12
    k = 8
    p = "10011"
    # data = 2^(n-k) data
    data = add_padding_zero(msg, n-k)
    # data % p
    remainder = divide_modulo_two(data, p)
    # FCS should have n-k bits
    return add_zeros(remainder, (n-k) - len(remainder))


def add_padding_zero(data, count):
    return data + "".join(list(repeat("0", count)))


def add_zeros(data, count):
    return "".join(list(repeat("0", count))) + data


def sum_modulo_two(a, b):
    result = ""
    # make their length equal
    if len(a) > len(b):
        add_zeros(b, len(a) - len(b))
    elif len(a) < len(b):
        add_zeros(a, len(b) - len(a))

    return xor(a, b, len(a))


def xor(a, b, n):
    return "".join(["0" if a[i] == b[i] else "1" for i in range(n)])


def divide_modulo_two(divider, divisor):
    remain = divider
    remain = remove_first_zeros(remain)
    divisor = remove_first_zeros(divisor)

    # division
    while len(remain) >= len(divisor):
        divisor_mul = add_padding_zero(divisor, len(remain) - len(divisor))
        remain = sum_modulo_two(remain, divisor_mul)
        remain = remove_first_zeros(remain)

    return remain


def remove_first_zeros(num):
    while num[0] == "0":
        if len(num) == 1:
            break
        num = num[1:]
    return num
