import pytest

from solution import computeArea


def test1():
    assert computeArea(-3, 0, -3, 4, 0, -1, 9, 2) == 45
    
def test2():
    assert computeArea(-2, -2, 2, 2, -2, -2, 2, 2) == 16