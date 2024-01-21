"""Test engine."""

from corvic import engine


def test_trivial():
    assert engine.sum_as_string(1, 2) == "3"
