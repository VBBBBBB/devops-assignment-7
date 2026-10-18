"""Automated tests executed by the Jenkins 'Test' stage."""

import pytest

from app import add, greet, is_even


def test_greet_default():
    assert greet() == "Hello, DevOps!"


def test_greet_custom_name():
    assert greet("Jenkins") == "Hello, Jenkins!"


def test_greet_empty_raises():
    with pytest.raises(ValueError):
        greet("")


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False
