
from math import ceil, sqrt

__all__ = ["text_to_bf"]

def text_to_bf(text: str) -> str:
    """
    Return Brainfuck code that prints the input text.
    The text has to be pure ASCII.
    """
    if not text:
        return ""

    # Initialize with the first character's value
    code = bf_print(ord(text[0]), 1)
    previous_value = ord(text[0])

    # Iterate over the text and generate Brainfuck code for the difference in ASCII values
    for char in text[1:]:
        current_value = ord(char)
        dif = current_value - previous_value
        code += bf_print(dif)
        previous_value = current_value

    return code


def bf_num(n: int) -> str:
    """Return brainfuck code that adds n"""

    symbol = "+" if n > 0 else "-"
    return abs(n)*symbol


def bf_mult(x: int, y: int) -> str:
    """Return the brainfuck code of x*y"""

    sign = 1 if x * y > 0 else -1
    return f"{bf_num(abs(x))}[>{bf_num(sign * abs(y))}<-]>"



def bf_tuple(x: int, y: int, z: int, pos: int=2) -> str:
    """
    Return brainfuck code that sums x*y+z to the second
    position of the tape and prints the final value.
    The position 1 has to be 0. The pointer's final state
    is 2. The initial state can be 1 or 2.

    pos: the initial position of the pointer (default 2)
    """

    move_pointer = ">" if pos == 1 else "<" if pos == 2 and y != 1 else ""
    return f"{move_pointer}{bf_num(x) if y == 1 else bf_mult(x, y)}{bf_num(z)}"


def triple(n: int) -> tuple[int, int, int]:
    """
    Return the optimal representation of n > 0
    that minimizes |x| + |y| + |z| with n = x * y + z
    """
    absn = abs(n)
    sq = int(ceil(sqrt(absn)))

    x, y, z = 0, 0, absn
    min_weight = absn

    for i in range(sq, 1, -1):
        j = absn // i
        k = absn - i * j
        weight = i + j + abs(k)

        if weight < min_weight:
            min_weight = weight
            x, y, z = i, j, k

    return (x, y, z) if x < y else (y, x, z)

def bf_print(n: int, pos: int = 2) -> str:
    """
    Return Brainfuck code that sums n to the second
    Brainfuck cell and prints the value.
    """

    x, y, z = triple(abs(n))
    sign = 1 if n >= 0 else -1

    code_sum = f"{bf_tuple(n, 1, 0, pos)}."
    code_triple = f"{bf_tuple(x, sign * y, sign * z, pos)}."

    return code_triple if len(code_triple) < len(code_sum) else code_sum
