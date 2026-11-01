#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Python titlecase usage tests.
"""

# pylint: disable=missing-function-docstring, wrong-import-position

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
import titlecase


def main():
    do_tests()


def do_tests():
    test1()
    test2()


def test1():
    print(
        "titlecase test1:", titlecase.titlecase("my title case"),
        end="\n\n",
    )


def test2():
    sample = "my iphone uses github api"
    obj = titlecase.EnglishTitleCase()
    res = obj.convert(sample)
    print("Original: ", sample)
    print("TitleCase:", res)
    num = obj.num_conversions()
    print(f"Converted: {num} words, {('FAIL', 'OK')[num == 3]}")
    assert num == 3, "Strange!"
    is_ok = titlecase.EnglishStatic().is_title_case(res)
    assert is_ok, res
    titled = titlecase.EnglishStatic().fallback(
        "My Iphone Uses Github Api",	# wrong title, just like Python title() does
    )
    is_ok = titled == sample.title()
    #print("Debug:", is_ok, ":", [titled], "vs", [sample.title()])
    assert is_ok, "EnglishStatic fallback() is bad."


if __name__ == '__main__':
    main()
