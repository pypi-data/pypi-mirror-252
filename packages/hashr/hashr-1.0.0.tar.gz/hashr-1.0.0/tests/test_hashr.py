import unittest
from unittest.mock import patch
from hashr import hashr, saltr, number_to_letters
from hashr.main import _main
import subprocess


class TestHashr(unittest.TestCase):
    def test_hashr(self):
        # test known hash result of "Hello World!"
        hash = hashr("Hello World!")
        self.assertEqual(hash, "brclfmetdrenfrctfpesdnckfojt")
        empty_hash = hashr("")
        self.assertEqual(empty_hash, "")
        another_hash = hashr("Hello World1")
        self.assertNotEqual(hash, another_hash)

    def test_saltr(self):
        number_salt = int(saltr(False))
        letter_salt = saltr()
        self.assertLess(999999, number_salt)
        self.assertGreater(10000000, number_salt)
        self.assertIs(type(letter_salt), str)

    def test_number_to_letters(self):
        letters = number_to_letters(12345)
        zero = number_to_letters(0)
        self.assertEqual(letters, "alcne")
        self.assertEqual(zero, "j")

    @patch("builtins.print")
    @patch("sys.argv", ["test_hashr.py", "test_input", "-s"])
    @patch("hashr.saltr", return_value="iqirioc")
    def test_main_with_salt(self, mock_saltr, mock_print):
        _main()
        expected_output = "Hash: esakanhqcpimgmencocpgnhtfnal\nSalt: iqirioc"
        mock_print.assert_called_once_with(expected_output)

    @patch("builtins.print")
    @patch("sys.argv", ["test_hashr.py", "test_input"])
    def test_main_without_salt(self, mock_print):
        _main()
        expected_output = "Hash: atfoamfpjpdqfkcndmgthmimengmj"
        mock_print.assert_called_once_with(expected_output)

    @patch("builtins.print")
    @patch("sys.argv", ["test_hashr.py", ""])
    def test_main_missing_input(self, mock_print):
        with self.assertRaises(SystemExit) as context:
            _main()
        self.assertEqual(context.exception.code, 1)
        mock_print.assert_called_once_with("Error: Input string is required.")

    def test_main_execution(self):
        result = subprocess.run(["python3", "hashr/main.py", "Hello World!"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "Hash: brclfmetdrenfrctfpesdnckfojt\n")


if __name__ == "__main__":
    unittest.main()
