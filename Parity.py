def compute_parity(msg):
    total = 0
    for bit in msg:
        total += int(bit)
    return total % 2


def compute_column_parity(total_msg):

    totals = [0] * len(total_msg[0])

    for i in range(len(total_msg)):
        for j in range(len(total_msg[i])):
            # sum of each column
            totals[j] += int(total_msg[i][j])

    # parity of each column
    parities = [totals[i] % 2 for i in range(len(totals))]
    # adding total parity bit
    parities.append(sum(parities) % 2)
    # convert to string sequence
    return "".join([str(parity) for parity in parities])
