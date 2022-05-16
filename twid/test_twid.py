import unittest

from twid import TwID


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.tw_id = TwID()

    def test_valid_format(self):
        self.assertEqual(True, self.tw_id.valid('A123456789'))

    def test_invalidformat(self):
        self.assertEqual(False, self.tw_id.valid(''))

    def test_miss_first(self):
        self.assertEqual(False, self.tw_id.valid('123456789'))

    def test_missing_num(self):
        self.assertEqual(False, self.tw_id.valid('A123'))

    def test_valid_check(self):
        self.assertEqual(True, self.tw_id.valid('W208404174'))

    def test_invalid_check(self):
        self.assertEqual(False, self.tw_id.valid('W208404173'))


if __name__ == '__main__':
    unittest.main()
