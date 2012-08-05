#!/usr/bin/python
import unittest

from reader import Summer


class SummerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = Summer()
    def assert_input(self, input, output):
        result = self.s.readline(input)
        self.assertEqual(result, output)
    def ensure_input(self, input):
        result = self.s.readline(input)
        self.assertEqual(result, input)

class TestBasics(SummerTestCase):
    def test_runthru(self):
        self.s.readline("hello 10 nums or 20 not.\n")
        self.s.readline("again 2 nums but not -54.345e")

    def test_basic_summing(self):
        """basic summing"""
        self.ensure_input("<@sum = 0>")
        self.s.readline("i've got 99 problems")
        self.s.readline("but summer ain't 1 of them.")
        self.ensure_input( "<@sum = 100>--")
        self.s.readline("reduce -20")
        self.ensure_input( "<@sum = 80>--")

    def test_arithmetics(self):
        self.ensure_input("<10/5 = 2>")
        self.ensure_input("<123+7 = 130>")
        self.ensure_input("<9*4 = 36>")
        self.ensure_input("<(100/3)*9 = 300>")

    def test_variables(self):
        self.s.readline("@car 4600 $")
        self.s.readline("@tires <4*150> $")
        self.s.readline("@tkt 2.5e10")
        self.ensure_input("<@tires = 600>")
        self.assert_input("<@tires>", "<@tires = 600>")
        self.ensure_input("<@car+@tires = 5200>")
        self.ensure_input("<@tkt = 2.5e+10>") #not very solid

    def test_typed_sums(self):
        """test summing of numbers of specific type."""
        self.s.readline("10 balls")
        self.s.readline("5 bikes")
        self.s.readline("5 balls")
        self.ensure_input("<@sum:balls = 15>")
        self.ensure_input("<@sum:bikes = 5>")
        self.ensure_input("<@sum:balls + @sum:bikes = 20>")


class TestMultievals(SummerTestCase):
    """test multiple evals and defs in a line."""

    def test_multiple_evals(self):
        """test plain sums"""
        self.s.readline("10 balls 15 bikes 4 euros")
        self.ensure_input("<@sum:balls = 10>")
        self.ensure_input("<@sum:bikes = 15>")
        self.ensure_input("<@sum:euros = 4>")

    def test_multiple_defs(self):
        self.s.readline("@balls 10 @dogs 3")
        self.ensure_input("<@balls+@dogs = 13>")

    def test_refs_within_line(self):
      self.s.readline("@foo 10 @bar <@foo*3>")
      self.ensure_input("<@bar = 30>")

    def test_sums_within_line(self):
       self.ensure_input("10 20 30 40 <@sum = 100>")

if __name__ == '__main__':
    unittest.main()
