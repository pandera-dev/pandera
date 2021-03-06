"""Tests individual model components."""

from typing import Any

import pytest

import pandera as pa


def test_field_to_column():
    """Test that Field outputs the correct column options."""
    for flag in ["nullable", "allow_duplicates", "coerce", "regex"]:
        for value in [True, False]:
            col = pa.Field(**{flag: value}).to_column(
                pa.DateTime, required=value
            )
            assert isinstance(col, pa.Column)
            assert col.dtype == pa.DateTime.value
            assert col.properties[flag] == value
            assert col.required == value


def test_field_to_index():
    """Test that Field outputs the correct index options."""
    for flag in ["nullable", "allow_duplicates"]:
        for value in [True, False]:
            index = pa.Field(**{flag: value}).to_index(pa.DateTime)
            assert isinstance(index, pa.Index)
            assert index.dtype == pa.DateTime.value
            assert getattr(index, flag) == value


def test_field_no_checks():
    """Test Field without checks."""
    assert not pa.Field().to_column(str).checks


@pytest.mark.parametrize(
    "arg,value,expected",
    [
        ("eq", 9, pa.Check.equal_to(9)),
        ("ne", 9, pa.Check.not_equal_to(9)),
        ("gt", 9, pa.Check.greater_than(9)),
        ("ge", 9, pa.Check.greater_than_or_equal_to(9)),
        ("lt", 9, pa.Check.less_than(9)),
        ("le", 9, pa.Check.less_than_or_equal_to(9)),
        (
            "in_range",
            {"min_value": 1, "max_value": 9},
            pa.Check.in_range(1, 9),
        ),
        ("isin", [9, "a"], pa.Check.isin([9, "a"])),
        ("notin", [9, "a"], pa.Check.notin([9, "a"])),
        ("str_contains", "a", pa.Check.str_contains("a")),
        ("str_endswith", "a", pa.Check.str_endswith("a")),
        ("str_matches", "a", pa.Check.str_matches("a")),
        (
            "str_length",
            {"min_value": 1, "max_value": 9},
            pa.Check.str_length(1, 9),
        ),
        ("str_startswith", "a", pa.Check.str_startswith("a")),
    ],
)
def test_field_checks(arg: str, value: Any, expected: pa.Check):
    """Test that all built-in checks are available in a Field."""
    checks = pa.Field(**{arg: value}).to_column(str).checks
    assert len(checks) == 1
    assert checks[0] == expected
