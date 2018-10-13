#!/usr/bin/env python3
import os
import lab
import json
import unittest
import doctest
from copy import deepcopy

import sys
sys.setrecursionlimit(10000)

TEST_DIRECTORY = os.path.dirname(__file__)

TESTDOC_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
TESTDOC_SKIP = ["lab", "lab.HyperMinesGame", "lab.HyperMinesGame.dump",
                "lab.HyperMinesGame.from_dict"]


class TestDocTests(unittest.TestCase):
    def test_doctests_run(self):
        """ Checking to see if all lab doctests run successfully """
        results = doctest.testmod(lab, optionflags=TESTDOC_FLAGS, report=False)
        self.assertEqual(results[0], 0)

    def test_all_doc_strings_exist(self):
        """ Checking if docstrings have been written for everything in lab.py """
        tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
        for test in tests:
            if test.name in TESTDOC_SKIP:
                continue
            if not test.docstring:
                self.fail("Oh no, '{}' has no docstring!".format(test.name))

    def test_all_doc_tests_exist(self):
        """ Checking if doctests have been written for everything in lab.py """
        tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
        for test in tests:
            if test.name in TESTDOC_SKIP:
                continue
            if not test.examples:
                self.fail("Oh no, '{}' has no doctests!".format(test.name))


class TestNewGame(unittest.TestCase):
    def test_newsmall6dgame(self):
        """ Testing new_game on a small 6-D board """
        with open("test_outputs/test_newsmall6dgame.json") as f:
            expected = json.load(f)
        with open("test_inputs/test_newsmall6dgame.json") as f:
            inputs = json.load(f)
        result = lab.HyperMinesGame(inputs["dimensions"], inputs["bombs"])
        for i in ('dimensions', 'board', 'mask', 'state'):
            self.assertEqual(getattr(result, i), expected[i])


    def test_newlarge4dgame(self):
        """ Testing new_game on a large 4-D board """
        with open("test_outputs/test_newlarge4dgame.json") as f:
            expected = json.load(f)
        with open("test_inputs/test_newlarge4dgame.json") as f:
            inputs = json.load(f)
        result = lab.HyperMinesGame(inputs["dimensions"], inputs["bombs"])
        for i in ('dimensions', 'board', 'mask', 'state'):
            self.assertEqual(getattr(result, i), expected[i])


class TestIntegration(unittest.TestCase):
    def _test_integration(self, n):
        with open("test_outputs/test_integration%s.json" % n) as f:
            expected = json.load(f)
        with open("test_inputs/test_integration%s.json" % n) as f:
            inputs = json.load(f)
        g = lab.HyperMinesGame(inputs['dimensions'], inputs['bombs'])
        for location, results in zip(inputs['digs'], expected):
            squares_revealed, game, rendered, rendered_xray = results
            res = g.dig(location)
            self.assertEqual(res, squares_revealed)
            for i in ('dimensions', 'board', 'mask', 'state'):
                self.assertEqual(getattr(g, i), game[i])
            self.assertEqual(g.render(), rendered)
            self.assertEqual(g.render(True), rendered_xray)

    def test_integration1(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(1)

    def test_integration2(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(2)

    def test_integration3(self):
        """ dig and render, repeatedly, on a large board"""
        self._test_integration(3)


class TestTiny(unittest.TestCase):
    """
    Your additional test cases for lab 4 should go here.
    """
    def test_1D(self):
        game = lab.HyperMinesGame([5],[[0],[3]])
        
        dig_result = game.dig([2])
        dig_expected = 1
        
        state_result = game.state
        expected_state = "ongoing"

        dig_result2 = game.dig([0])
        dig_expected2 = 1

        state_result2 = game.state
        expected_state2 = "defeat"
        
        self.assertEqual(dig_result, dig_expected)
        self.assertEqual(dig_result2, dig_expected2)
        self.assertEqual(state_result, expected_state)
        self.assertEqual(state_result2, expected_state2)

    def test_2D(self):
        game = lab.HyperMinesGame([3,3],[[0,2],[0,0]])
        
        dig_result = game.dig([0,1])
        dig_expected = 1

        dig_result2 = game.dig([2,0])
        dig_expected2 = 6

        self.assertEqual(dig_result, dig_expected)
        self.assertEqual(dig_result2, dig_expected2)

    def test_3D(self):
        game = lab.HyperMinesGame([3,3,2],[[1,2,0]])
        
        dig_result = game.dig([2,1,0])
        dig_expected = 1

        dig_result2 = game.dig([0,0,0])
        dig_expected2 = 11

        self.assertEqual(dig_result, dig_expected)
        self.assertEqual(dig_result2, dig_expected2)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
