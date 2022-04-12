from math import log2

"""
The purpose of the following functions is to look for hexadecimal sequences in pi.
If, somehow, the starting index of every sequences (of a given length) is shorter than the actual value
of the said sequences, then we can compress every piece of data, by storing the pi index instead of the
sequence itself.

Sadly, it is not the case.. :(
"""


"""
Following functions compute and return the nth digit of pi (hexadecimal form).
(Note: tbh I took this code from the internet)
"""


def bbp(digit_position: int, precision: int = 1000) -> str:
    if (not isinstance(digit_position, int)) or (digit_position <= 0):
        raise ValueError("Digit position must be a positive integer")
    elif (not isinstance(precision, int)) or (precision < 0):
        raise ValueError("Precision must be a non-negative integer")

    sum_result = (
        4 * _subsum(digit_position, 1, precision)
        - 2 * _subsum(digit_position, 4, precision)
        - _subsum(digit_position, 5, precision)
        - _subsum(digit_position, 6, precision)
    )
    return hex(int((sum_result % 1) * 16))[2:]


def _subsum(
    digit_pos_to_extract: int, denominator_addend: int, precision: int
) -> float:
    sums = 0.0
    for sum_index in range(digit_pos_to_extract + precision):
        denominator = 8 * sum_index + denominator_addend
        if sum_index < digit_pos_to_extract:
            exponential_term = pow(
                16, digit_pos_to_extract - 1 - sum_index, denominator
            )
        else:
            exponential_term = pow(16, digit_pos_to_extract - 1 - sum_index)
        sums += exponential_term / denominator
    return sums


def byte_storage(n: int) -> int:
    """
    Get the number of byte (8 bits) needed to store a positive integer "n".
    :param n: The said integer.
    :type n: int
    :return: the number of byte needed to store it.
    :rtype: int
    """
    assert n >= 0, "this function only works with positive integers"
    if n == 0:
        return 1

    return (int(log2(n)) + 1) // 8 + 1


def find_seq(seq: str) -> int:
    """
    Get the starting index of the first occurrence of the given sequence in pi's digits.
    :param seq: The sequence that you want to find in pi.
    :return: the index of the sequence in pi's digits.
    """
    i = 0
    while True:
        print(i, end="\r")
        i += 1
        if bbp(i) != seq[0]:
            continue

        found = True
        for j in range(1, len(seq)):
            if bbp(i+j) != seq[j]:
                found = False
                i += j
                break

        if found:
            break

    return i


def main():
    for i in range(2**16):
        pi_index = find_seq(hex(i)[2:])

        if byte_storage(pi_index) > byte_storage(i):
            print("[!] {} is larger to store using its pi index ({} bytes instead of {})"
                  .format(i, byte_storage(pi_index), byte_storage(i)))


main()
