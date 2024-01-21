from endi.utils.ascii import (
    force_ascii,
    force_filename,
)


def test_force_ascii():
    assert force_ascii(b"\xc3\xa9co") == "eco"
    assert force_ascii(5) == "5"
    assert force_ascii("éco") == "eco"


def test_force_filename():
    assert force_filename("é' ';^") == "e_"
