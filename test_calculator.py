import unittest
import calculator


class TestCalculator(unittest.TestCase):
    def test_split_string(self):
        self.assertEqual(calculator.split_string("1 +++ 2 * 3 -- 4"), ["1", "+++", "2", "*", "3", "--", "4"])
        self.assertEqual(calculator.split_string("2 *** 3"), ["2", "***", "3"])
        self.assertEqual(calculator.split_string("-10"), ["-", "10"])
        self.assertEqual(calculator.split_string("2 + -3"), ["2", "+-", "3"])
        self.assertEqual(calculator.split_string("8 + 12 * (4 - 2)"), ["8", "+", "12", "*", "(", "4", "-", "2", ")"])
        self.assertEqual(calculator.split_string("c*(2+3)"), ["c", "*", "(", "2", "+", "3", ")"])
        self.assertEqual(calculator.split_string("a+(3*(1+2))"), ["a", "+", "(", "3", "*", "(", "1", "+", "2", ")", ")"])

    def test_variable_valid(self):
        self.assertFalse(calculator.variable_valid(["c4", "*", "(", "2", "+", "3", ")"]))
        self.assertFalse(calculator.variable_valid(["a", "+", "(", "3", "*", "(", "1", "+", "2", ")", ")"]))
        self.assertTrue(calculator.variable_valid(["2", "***", "3"]))

    def test_handle_operators(self):
        self.assertEqual(calculator.handle_operators([2, "+++", 3]), [2, "+", 3])
        self.assertEqual(calculator.handle_operators([2, "--", 3]), [2, "+", 3])
        self.assertEqual(calculator.handle_operators([2, "---", 3]), [2, "-", 3])
        self.assertEqual(calculator.handle_operators([2, "-+", 3]), [2, "-", 3])
        self.assertEqual(calculator.handle_operators([2, "+-", 3]), [2, "-", 3])
        self.assertIsNone(calculator.handle_operators([2, "***", 3]))
        self.assertIsNone(calculator.handle_operators([2, "+++-", 3]))
        self.assertIsNone(calculator.handle_operators([2, "***", "(", 3]))
        self.assertIsNone(calculator.handle_operators([2, "**/", 3]))

    def test_start_end_valid(self):
        self.assertFalse(calculator.start_end_valid(["+", 3]))

    def test_infix_to_postfix(self):
        self.assertEqual(calculator.infix_to_postfix(['x', '+', 'y', '-', 5]), ['x', 'y', '+', 5, '-'])
        self.assertEqual(calculator.infix_to_postfix(['x', '+', '(', 'y', '-', 5, ')']), ['x', 'y', 5, '-', '+'])
        self.assertEqual(calculator.infix_to_postfix(['x', '+', 'y', '*', 5]), ['x', 'y', 5, '*', '+'])
        self.assertEqual(calculator.infix_to_postfix(['x', '*', 'y', '-', 5]), ['x', 'y', '*', 5, '-'])
        self.assertEqual(calculator.infix_to_postfix([3, '+', 2, '*', 4]), [3, 2, 4, '*', '+'])
        self.assertEqual(calculator.infix_to_postfix([2, '*', '(', 3, '+', 4, ')', '+', 1]), [2, 3, 4, '+', '*', 1, '+'])
        self.assertEqual(calculator.infix_to_postfix([8, '*', 3, '+', 12, '*', '(', 4, '-', 2, ')']),
                         [8, 3, '*', 12, 4, 2, '-', '*', '+'])

    def test_basic_calculation(self):
        self.assertEqual(calculator.basic_calculation(3, 5, "+"), 8)
        self.assertEqual(calculator.basic_calculation(3, 5, "-"), -2)
        self.assertEqual(calculator.basic_calculation(3, 5, "*"), 15)
        self.assertEqual(calculator.basic_calculation(5, 3, "/"), 2)

    def test_calculate(self):
        self.assertEqual(calculator.calculate([3, 2, 4, '*', '+']), 11)
        self.assertEqual(calculator.calculate([2, 3, 4, '+', '*', 1, '+']), 15)
        self.assertEqual(calculator.calculate([8, 3, '*', 12, 4, 2, '-', '*', '+']), 48)


if __name__ == "__main__":
    unittest.main()