
import pytest

from customs_duty import duty_rate, total_duty, clearance_channel


# DUTY RATE TESTS

def test_prohibited_weapons():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")


def test_prohibited_narcotics():
    with pytest.raises(ValueError):
        duty_rate("narcotics", "US")


def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta():
    assert duty_rate("clothing", "US") == 0.12


def test_books():
    assert duty_rate("books", "US") == 0


def test_unknown_category():
    assert duty_rate("furniture", "US") == 0.15


# TOTAL DUTY TESTS

def test_negative_value():
    with pytest.raises(ValueError):
        total_duty("books", -10, "US", False)


def test_non_negative_value():
    assert total_duty("books", 2000, "US", False) == 0


def test_gift_within_limit():
    assert total_duty("electronics", 5000, "FTA", True) == 0


def test_gift_above_limit():
    assert total_duty("electronics", 5100, "FTA", True) == 50


def test_non_gift_within_limit():
    assert total_duty("electronics", 1000, "FTA", False) == 0


def test_non_gift_above_limit():
    assert total_duty("electronics", 2000, "FTA", False) == 200


def test_minimum_duty():
    assert total_duty("electronics", 5100, "FTA", True) == 50


def test_duty_zero():
    assert total_duty("books", 2000, "US", False) == 0


def test_duty_above_minimum():
    assert total_duty("electronics", 6000, "FTA", True) == 100


# CLEARANCE CHANNEL TESTS

def test_prohibited_clearance():
    assert clearance_channel(500, "weapons", True) == "refuse"


def test_allowed_clearance():
    assert clearance_channel(500, "electronics", True) == "green"


def test_value_above_100000():
    assert clearance_channel(150000, "electronics", True) == "inspect"


def test_value_below_100000():
    assert clearance_channel(50000, "electronics", True) == "green"


def test_missing_documents():
    assert clearance_channel(50000, "electronics", False) == "inspect"


def test_documents_available():
    assert clearance_channel(50000, "electronics", True) == "green"


def test_value_equal_to_20000():
    assert clearance_channel(20000, "electronics", False) == "green"
