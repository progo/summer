#!/usr/bin/python
import unittest

from reader import Summer


class SummerTestCase(unittest.TestCase):
    def setUp(self):
        self.s = Summer()
    def assert_input(self, input, output):
        result = self.s.readline(input)
        self.assertEqual(result, output)

class TestBasics(SummerTestCase):
    def test_runthru(self):
        self.s.readline("hello 10 nums or 20 not.\n")
        self.s.readline("again 2 nums but not -54.345e")

    def test_basic_summing(self):
        """basic summing"""
        self.assert_input("<@sum>", "<@sum = 0>")
        self.s.readline("i've got 99 problems")
        self.s.readline("but summer ain't 1 of them.")
        self.assert_input("<@sum>--",  "<@sum = 100>--")
        self.s.readline("reduce -20")
        self.assert_input("<@sum>--",  "<@sum = 80>--")

    def test_arithmetics(self):
        self.assert_input("<10/5>", "<10/5 = 2>")
        self.assert_input("<123+7>", "<123+7 = 130>")
        self.assert_input("<9*4>", "<9*4 = 36>")
        self.assert_input("<(100/3)*9>", "<(100/3)*9 = 300>")

    def test_variables(self):
        self.s.readline("@car 4600 $")
        self.s.readline("@tires <4*150> $")
        self.s.readline("@tkt 2.5e10")
        self.assert_input("<@tires>", "<@tires = 600>")
        self.assert_input("<@car+@tires>", "<@car+@tires = 5200>")
        self.assert_input("<@tkt>", "<@tkt = 2.5e+10>") #not very solid

    def test_typed_sums(self):
        """test summing of numbers of specific type."""
        self.s.readline("10 balls")
        self.s.readline("5 bikes")
        self.s.readline("5 balls")
        self.assert_input("<@sum:balls>", "<@sum:balls = 15>")
        self.assert_input("<@sum:bikes>", "<@sum:bikes = 5>")
        self.assert_input("<@sum:balls + @sum:bikes>",
                "<@sum:balls + @sum:bikes = 20>")


class TestMultievals(SummerTestCase):
    """test multiple evals and defs in a line."""

    def test_multiple_evals(self):
        """test plain sums"""
        self.s.readline("10 balls 15 bikes 4 euros")
        self.assert_input("<@sum:balls>", "<@sum:balls = 10>")
        self.assert_input("<@sum:bikes>", "<@sum:bikes = 15>")
        self.assert_input("<@sum:euros>", "<@sum:euros = 4>")

    def test_multiple_defs(self):
        self.s.readline("@balls 10 @dogs 3")
        self.assert_input("<@balls+@dogs>","<@balls+@dogs = 13>")
        #self.s.readline("@foo 10 @bar <@foo*3>")
        #self.assert_input("<@bar>", "<@bar = 30>")



# some helpful tests for 'nums'. Should be removed after we're finished because
# they're not black box tests.
from nums import Number, grab_numbers
class TestNums(unittest.TestCase):
    def test_number_grabbing(self):
        self.assertEqual(grab_numbers("i've got 99 problems"),
                [Number(val=99.0, type='problems')])
        self.assertEqual(grab_numbers("1 2 3"),
                [Number(val=1.0, type=''),
                 Number(val=2.0, type=''),
                 Number(val=3.0, type='')])

    def test_type_grabbing(self):
        self.assertEqual(grab_numbers("12 op"),
                [Number(val=12.0, type='op')])
        self.assertEqual(grab_numbers("<12*4 = 48> eur"),
                [Number(val=48.0, type='eur')])

    def test_floats(self):
        """floating point numbers are tough."""
        self.assertEqual(grab_numbers("1.5"),
                [Number(val=1.5, type='')])
        self.assertEqual(len(grab_numbers("1.4 2.4 0.3 4")), 4)

if __name__ == '__main__':
    unittest.main()
