
import unittest
from newline-api import example_function

class TestNewline-api(unittest.TestCase):
    def test_example_function(self):
        self.assertEqual(example_function(), "Hello from newline-api!")

if __name__ == '__main__':
    unittest.main()
