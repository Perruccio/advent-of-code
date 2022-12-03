import unittest
import sys
import pathlib

curr_dir = pathlib.Path(__file__).parent.parent
sys.path.append(str(curr_dir))

from day02 import solution


class Test(unittest.TestCase):
    def test(self):
        p1, p2 = solution.main()
        self.assertEqual(p1, 8890)
        self.assertEqual(p2, 10238)


if __name__ == "__main__":
    unittest.main()
