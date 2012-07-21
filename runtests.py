#!/usr/bin/python
import unittest

from reader import Summer

class TestBasics(unittest.TestCase):
    def test_runthru(self):
        summer = Summer()
        summer.readline("hello 10 nums or 20 not.\n")
        summer.readline("again 2 nums but not -54.345e")

    def test_summing(self):
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
        ae("<@tires>", "<@tires = 600>")
        ae("<@car+@tires>", "<@car+@tires = 5200>")


if __name__ == '__main__':
    unittest.main()
