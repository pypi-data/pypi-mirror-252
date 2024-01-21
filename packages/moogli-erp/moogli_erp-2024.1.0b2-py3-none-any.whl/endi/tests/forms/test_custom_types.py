import colander
from endi.forms.custom_types import AmountType
from endi.forms.custom_types import specialfloat
from endi.forms.custom_types import Integer


def test_amount_type():
    a = AmountType()
    assert a.serialize(None, 15000) == "150.0"
    assert a.deserialize(None, "79.4") == 7940
    assert a.deserialize(None, "292,65") == 29265


def test_specialfloat():
    a = "495, 4 5€"
    assert specialfloat("", a) == 495.45


def test_integer():
    i = Integer()
    assert colander.null == i.serialize(None, None)
    assert "0" == i.serialize(None, 0)


def test_csv_set():
    from endi.forms.custom_types import CsvTuple

    i = CsvTuple()

    assert colander.null == i.serialize(None, None)
    assert () == i.serialize(None, "")

    tuple_res = ("aa", "bb", "cc")
    str_res = "aa,bb,cc"

    assert i.serialize(None, str_res) == tuple_res
    assert i.deserialize(None, tuple_res) == str_res
