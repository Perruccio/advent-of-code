import unittest
import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(curr_dir))

from day01 import solution


class Test(unittest.TestCase):
    def test(self):
        p1, p2 = solution.main()
        self.assertEqual(p1, 72240)
        self.assertEqual(p2, 210957)


if __name__ == "__main__":
    unittest.main()
