from endi.compute.sage.base import double_lines, filter_accounting_entry


def decoratorfunc(a, b):
    return {"type_": "A", "key": "value", "num_analytique": "NUM"}


def test_double_lines():
    res = list(double_lines(decoratorfunc)(None, None))
    g, a = res
    assert res == [
        {"type_": "G", "key": "value", "_analytic_counterpart": a},
        {
            "type_": "A",
            "key": "value",
            "num_analytique": "NUM",
            "_general_counterpart": g,
        },
    ]


def test_filter_accounting_entry():
    assert filter_accounting_entry({"credit": -5}) == {"debit": 5}
    assert filter_accounting_entry({"debit": 5}) == {"debit": 5}
    assert filter_accounting_entry({"debit": -5}) == {"credit": 5}
    assert filter_accounting_entry({"credit": 5}) == {"credit": 5}
