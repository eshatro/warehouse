import pytest

from src.inventory.validators import *


@pytest.mark.parametrize(
    "design_input, expected",
    [
        ("AS2a2b3", True),
        ("BL2a2", True),
        ("ZS3b3c5", True),
    ],
)
def test_val_str(design_input, expected):
    is_valid, _ = val_str(design_input)
    assert is_valid is expected


@pytest.mark.parametrize(
    "flower_species, expected",
    [
        (1, True),
        ("ordaaaaaah!", False),
        ("1", True),
        ("Bs2a2@", False),
        ("12", True),
        ("abcdee", False),
    ],
)
def test_val_int(flower_species, expected):
    is_valid, _ = val_int(flower_species)
    assert is_valid is expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ("ab", False),
        (["bcd"], True),
        (1, False),
        ("213", False),
        (list("123"), True),
    ],
)
def test_check_type_list(data, expected):
    is_valid, _ = check_type(data)
    assert is_valid is expected
