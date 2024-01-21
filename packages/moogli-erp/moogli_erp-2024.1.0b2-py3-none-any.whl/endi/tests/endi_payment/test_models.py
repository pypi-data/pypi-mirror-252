import datetime


def test_as_csv(mk_payment_history):
    e = mk_payment_history()
    assert isinstance(e.as_csv(), str)


def test_serialize(mk_payment_history):
    e = mk_payment_history()
    assert isinstance(e.serialize(), str)


def test_as_binary(mk_payment_history):
    e = mk_payment_history()
    assert isinstance(e.as_binary(), bytes)
