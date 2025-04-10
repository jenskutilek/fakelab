from __future__ import annotations

import unittest

import pytest

from FL.helpers.FLList import FLList, adjust_list


class FLListTests(unittest.TestCase):
    def test_adjust_list_equal(self):
        seq = [0, 0, 0, 0]
        expected = [0, 0, 0, 0]
        adjust_list(seq, 4)
        assert seq == expected

    def test_adjust_list_empty(self):
        seq = []
        expected = [None, None, None]
        adjust_list(seq, 3)
        assert seq == expected

    def test_adjust_list_empty_value(self):
        seq = []
        expected = [0, 0, 0]
        adjust_list(seq, 3, 0)
        assert seq == expected

    def test_adjust_list_no_value(self):
        seq = [0]
        expected = [0, 0, 0]
        adjust_list(seq, 3)
        assert seq == expected

    def test_adjust_list_value(self):
        seq = [1]
        expected = [1, 0, 0]
        adjust_list(seq, 3, 0)
        assert seq == expected

    def test_adjust_list_shorter_no_value(self):
        seq = [0, 0, 0]
        expected = [0]
        adjust_list(seq, 1)
        assert seq == expected

    def test_adjust_list_shorter_value(self):
        seq = [1, 0, 0]
        expected = [1]
        adjust_list(seq, 1, 0)  # value is ignored
        assert seq == expected
