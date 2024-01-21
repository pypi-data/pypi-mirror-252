import pytest


def test_parser():
    from endi.compute.parser import NumericStringParser

    parser = NumericStringParser()

    assert parser.parse("2 * 4 / 100.0") == ["2", "4", "*", "100.0", "/"]
    assert parser.parse("100.0 / 3") == ["100.0", "3", "/"]
    assert parser.parse("100.0 / (3 + 2)") == ["100.0", "3", "2", "+", "/"]
    assert parser.parse("100.0 / {fu éo}") == ["100.0", "{fu éo}", "/"]

    with pytest.raises(Exception):
        parser.parse("__import__('os').remove('/tmp/titi')")


def test_float_reducer():
    from endi.compute.parser import NumericStringFloatReducer

    reducer = NumericStringFloatReducer

    assert reducer.reduce(["2", "4", "*", "100.0", "/"]) == 0.08
    assert int(reducer.reduce(["100.0", "3", "/"])) == 33
    assert reducer.reduce(["100.0", "2", "3", "+", "/"]) == 20

    with pytest.raises(SyntaxError):
        reducer.reduce(["{fu}"])
