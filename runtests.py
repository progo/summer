#!/usr/bin/python
import unittest

from reader import Summer

class TestBasics(unittest.TestCase):
    def test_runthru(self):
        summer = Summer()
        summer.readline("hello 10 nums or 20 not.\n")
        summer.readline("again 2 nums but not -54.345e")

    def test_basic_summing(self):
        """in these tests we're concerned only with the last numbers in each
        line."""
        s = Summer()
        s.readline("i've got 99 problems")
        s.readline("but summer ain't 1 of them.")
        self.assertEqual(s.readline("<@sum>--"), "<@sum = 100>--")
        s.readline("reduce -20")
        self.assertEqual(s.readline("<@sum>--"), "<@sum = 80>--")

    def test_arithmetics(self):
        s = Summer()
        def ae(input, output):
            self.assertEqual(s.readline(input), output)
        ae("<10/5>", "<10/5 = 2>")
        ae("<123+7>", "<123+7 = 130>")
        ae("<9*4>", "<9*4 = 36>")
        ae("<(100/3)*9>", "<(100/3)*9 = 300>")

    def test_variables(self):
        s = Summer()
        def ae(input, output):
            self.assertEqual(s.readline(input), output)
        s.readline("@car 4600 $")
        s.readline("@tires <4*150> $")
        s.readline("@tkt 2.5e10")
        ae("<@tires>", "<@tires = 600>")
        ae("<@car+@tires>", "<@car+@tires = 5200>")
        ae("<@tkt>", "<@tkt = 2.5e+10>") #not very solid

    def test_typed_sums(self):
        """test summing of numbers of specific type."""
        s = Summer()
        def ae(input, output):
            self.assertEqual(s.readline(input), output)
        s.readline("10 balls")
        s.readline("5 bikes")
        s.readline("5 balls")
        ae("<@sum:balls>", "<@sum:balls = 15>")
        ae("<@sum:bikes>", "<@sum:bikes = 5>")
        ae("<@sum:balls + @sum:bikes>", "<@sum:balls + @sum:bikes = 20>")


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
