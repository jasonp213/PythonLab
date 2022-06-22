import unittest

from stackqueue import StackQueue


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.queue = StackQueue()
        self.elements = iter(range(10))

    def test_put1_pop1(self):
        e1 = self.given_element()
        self.assertEqual(self.queue.pop(), e1)

    def test_put2_pop2(self):
        e1 = self.given_element()
        e2 = self.given_element()
        self.assertEqual(self.queue.pop(), e1)
        self.assertEqual(self.queue.pop(), e2)

    def test_put2_pop1_put1_pop1(self):
        e1 = self.given_element()
        e2 = self.given_element()
        self.assertEqual(self.queue.pop(), e1)
        e3 = self.given_element()
        self.assertEqual(self.queue.pop(), e2)
        self.assertEqual(self.queue.pop(), e3)

    def given_element(self):
        element = next(self.elements)
        self.queue.put(element)
        return element
