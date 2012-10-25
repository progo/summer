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
    """test the basic functionality: evaluating calculations and summings."""

    def test_runthru(self):
        """musn't throw up."""
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

    def test_accumulation(self):
        """test if comments and acc characters work as intended."""
        self.s.readline("-- 120")
        self.s.readline("0.5 --")
        self.s.readline(";-- 120")
        self.s.readline(";160")
        self.s.readline("150;")
        self.ensure_input("<@sum = 150>")

    def test_arithmetics(self):
        """calc shouldn't get these wrong."""
        self.ensure_input("<10/5 = 2>")
        self.ensure_input("<123+7 = 130>")
        self.ensure_input("<9*4 = 36>")
        self.ensure_input("<(100/3)*9 = 300>")
        self.ensure_input("<1+1+1+1+1+1 = 6>")

    def test_expr_updating(self):
        """when exprs are updated, the results should update tidily."""
        self.assert_input("<12/3 =>",
                          "<12/3 = 4>")
        self.assert_input("<12/3 = >",
                          "<12/3 = 4>")
        self.assert_input("<12/3 = aybabtu>",
                          "<12/3 = 4>")
        self.assert_input("<12/3 = 5>",
                          "<12/3 = 4>")
        self.assert_input("<1004-4+10 = 4443>",
                          "<1004-4+10 = 1010>")

class TestVariables(SummerTestCase):
    """test defining and using @variables."""

    def test_variables(self):
        self.s.readline("@car 4600 $")
        self.s.readline("@tires <4*150> $")
        self.s.readline("@tkt 2.5e10")
        self.ensure_input("<@tires = 600>")
        self.assert_input("<@tires>", "<@tires = 600>")
        self.ensure_input("<@car+@tires = 5200>")
        self.ensure_input("<@tkt = 2.5e+10>") #not very solid

    def test_badly_named_variables(self):
        """should cope with names inside other names"""
        self.s.readline("@abc 123")
        self.s.readline("@cde 234")
        self.s.readline("@abcde 500")
        self.ensure_input("<@abcde = 500>")

    def test_updated_variable(self):
        """should set variable with new results."""
        self.s.readline("@new <100+10 = 105>")
        self.ensure_input("<@new = 110>")

class TestTypes(SummerTestCase):
    """test typed sums."""

    def test_typed_sums(self):
        """test summing of numbers of specific type."""
        self.s.readline("10 balls")
        self.s.readline("5 bikes")
        self.s.readline("5 balls")
        self.ensure_input("<@sum:balls = 15>")
        self.ensure_input("<@sum:bikes = 5>")
        self.ensure_input("<@sum:balls + @sum:bikes = 20>")

    def test_variables(self):
        """variables should assign fine."""
        self.s.readline("10 balls, 5 balls more.")
        self.ensure_input("<@sum:balls = 15>")
        self.s.readline("@balls <@sum:balls>")
        self.ensure_input("<@balls = 15>")

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

    def test_identical_exprs(self):
        """is this a bug or some sick misbehavior on user's behalf..."""
        self.s.readline("@a <12/3> @b <@sum> @c <@sum>")
        self.ensure_input("<@a = 4> <@b = 4> <@c = 8>")

class TestAnsFunctionality(SummerTestCase):
    """test recalling the last result in new expressions."""

    def test_single(self):
        self.s.readline("<123*10>")
        self.s.readline("<_ + 70>")
        self.ensure_input("<_ = 1300>")
        self.ensure_input("<_+_-2*_ = 0>")

    def test_corner_cases(self):
        self.s.readline("<100/2>")
        self.ensure_input("<_ = 50>")
        self.ensure_input("<_ = 50>")
        self.s.readline("@foo 30 pizzas")
        self.ensure_input("<_ = 50>")
        self.s.readline("<_ * 3>")
        self.ensure_input("<_ = 150>")

    def test_vars(self):
        self.s.readline("@var <100-50 = 50>")
        self.ensure_input("@newv <@var-2*_ = -50>")
        self.ensure_input("<@newv-_ = 0>")

    def test_synon(self):
        self.s.readline("<120 - 20>")
        self.ensure_input("<@ans - _ = 0>")


if __name__ == '__main__':
    unittest.main()
