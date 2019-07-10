# coding: utf-8


import pytest


def test_simple():
    assert True is True


@pytest.mark.skip
def test_simple_false():
    assert True is False
