import unittest

from brainfuck_art.brainfuck_generation import bf_num, bf_mult, bf_tuple, bf_print, text_to_bf, triple
from brainfuck_art.brainfuck_interpreter import execute_bf

class TestBrainfuckFunctions(unittest.TestCase):
    """
    Unit tests for Brainfuck-related functions, including bf_num, bf_mult, bf_tuple, triple, bf_print, and text_to_bf.
    These tests verify that the functions correctly generate Brainfuck code that produces the expected output and tape state.
    """

    def test_bf_num(self):
        """
        Test the bf_num function by generating Brainfuck code for positive, negative, and zero values.
        Verify that the resulting tape contains the correct value at the first memory cell.
        """
        # Test positive number
        with self.subTest(n=5):
            code = bf_num(5)
            _, tape = execute_bf(code)
            self.assertEqual(tape[0], 5)

        # Test negative number
        with self.subTest(n=-3):
            code = bf_num(-3)
            _, tape = execute_bf(code)
            self.assertEqual(tape[0], 253)  # 256 - 3

        # Test zero
        with self.subTest(n=0):
            code = bf_num(0)
            _, tape = execute_bf(code)
            self.assertEqual(tape[0], 0)

    def test_bf_mult(self):
        """
        Test the bf_mult function by generating Brainfuck code for the multiplication of two numbers.
        Verify that the resulting tape contains the correct value representing the product at the first memory cell.
        """
        # Test x * y for different values
        with self.subTest(x=2, y=3):
            code = bf_mult(2, 3)
            _, tape = execute_bf(code)
            self.assertEqual(tape[1], 6)

        with self.subTest(x=0, y=5):
            code = bf_mult(0, 5)
            _, tape = execute_bf(code)
            self.assertEqual(tape[1], 0)

    def test_bf_tuple(self):
        """
        Test the bf_tuple function by generating Brainfuck code for the expression x * y + z.
        Verify that the resulting tape contains the correct value representing the result at the second memory cell.
        """
        # Test x * y + z for different values
        with self.subTest(x=2, y=3, z=1):
            code = bf_tuple(2, 3, 1, pos=0)
            _, tape = execute_bf(code)
            self.assertEqual(tape[1], 7)

        with self.subTest(x=-2, y=3, z=-1):
            code = bf_tuple(-2, 3, -1, pos=0)
            _, tape = execute_bf(code)
            self.assertEqual(tape[1], 249)  # 256 - 7

        with self.subTest(x=0, y=4, z=0):
            code = bf_tuple(0, 5, 0, pos=0)
            _, tape = execute_bf(code)
            self.assertEqual(tape[1], 0)

    def test_triple(self):
        """
        Test the triple function by generating triplets (x, y, z) for different values of n.
        Verify that x * y + z equals n.
        """
        # Test the correctness of the triple function

        for n in range(256):
            with self.subTest(n=n):
                x, y, z = triple(n)
                self.assertEqual(x * y + z, n)


    def test_bf_print(self):
        """
        Test the bf_print function by generating Brainfuck code that prints a single character based on the input value.
        Verify that the output matches the expected character.
        """
        # Test bf_print for different values
        code = bf_print(5)
        output, _ = execute_bf(code)
        self.assertEqual(output, chr(5))

        code  = bf_print(-3)
        output, _ = execute_bf(code)
        self.assertEqual(output, chr(253))  # 256 - 3

        code = bf_print(0)
        output, _ = execute_bf(code)
        self.assertEqual(output, chr(0))

    def test_text_to_bf(self):
        """
        Test the text_to_bf function by generating Brainfuck code that prints a given text string.
        Verify that the output matches the input text.
        """
        # Test text_to_bf function
        text = "ABC"
        code = text_to_bf(text)
        output, _ = execute_bf(code)
        self.assertEqual(output, "ABC")

        text = "Hello, World!"
        code = text_to_bf(text)
        output, _ = execute_bf(code)
        self.assertEqual(output, "Hello, World!")

        text = ""
        code = text_to_bf(text)
        output, _ = execute_bf(code)
        self.assertEqual(output, "")

if __name__ == '__main__':
    unittest.main()
