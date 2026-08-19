"""Unit tests for pkgdemo core."""

import pytest
from pkgdemo.core import format_greeting, main


def test_format_greeting_valid():
    assert format_greeting("Alice") == "Hello, Alice! Welcome to Python Packaging."


def test_format_greeting_empty():
    with pytest.raises(ValueError, match="Name cannot be empty"):
        format_greeting("   ")


def test_main_cli(capsys):
    ret = main(["Bob"])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Hello, Bob!" in captured.out
