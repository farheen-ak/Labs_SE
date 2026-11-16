
import pytest
from hypothesis import given, strategies as st

from PES2UG24CS164_customs_duty import parse_declaration, duty_amount, hs_chapter


# Test 1: Parse declaration

@given(
    category=st.text().filter(
    lambda x: bool(x.strip()) and ":" not in x
),
    value=st.floats(min_value=0, max_value=100000,
                    allow_nan=False, allow_infinity=False)
)
def test_parse_declaration_valid(category, value):
    result = parse_declaration(f"{category}:{value}")
    assert result == (category.strip().lower(), value)


@pytest.mark.parametrize("bad", [
    None, "", ":10", "abc:x", "abc:-1", "a:1:2"
])
def test_parse_declaration_invalid(bad):
    with pytest.raises(ValueError):
        parse_declaration(bad)


# Test 2: Duty amount

@given(
    value=st.floats(min_value=0, max_value=100000,
                    allow_nan=False, allow_infinity=False),
    rate=st.floats(min_value=0, max_value=100,
                   allow_nan=False, allow_infinity=False)
)
def test_duty_amount_valid(value, rate):
    assert duty_amount(f"{value}@{rate}") == pytest.approx(
        value * rate / 100
    )


@pytest.mark.parametrize("bad", [
    None, "", "@", "abc@20", "10@abc",
    "-1@20", "10@-2", "1@2@3"
])
def test_duty_amount_invalid(bad):
    with pytest.raises(ValueError):
        duty_amount(bad)


# Test 3: HS chapter

@given(chapter=st.integers(min_value=0, max_value=99))
def test_hs_chapter_valid(chapter):
    assert hs_chapter(f"{chapter:02d}.12") == chapter


@pytest.mark.parametrize("bad", [
    None, "", "1.23", "abc.123", "8517.12.3"
])
def test_hs_chapter_invalid(bad):
    with pytest.raises(ValueError):
        hs_chapter(bad)
