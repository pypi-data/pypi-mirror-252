import datetime
import pytest


def test_parse_date():
    from endi.utils.datetimes import parse_date

    assert parse_date("2019-01-03") == datetime.date(2019, 1, 3)
    assert parse_date("2019-03-01", format_="%Y-%d-%m") == datetime.date(2019, 1, 3)

    assert parse_date("toto", default="") == ""

    with pytest.raises(ValueError):
        parse_date("toto")


def test_parse_datetime():
    from endi.utils.datetimes import parse_datetime

    assert parse_datetime("2019-01-01 12:15:20") == datetime.datetime(
        2019, 1, 1, 12, 15, 20
    )
    with pytest.raises(ValueError):
        assert parse_datetime("2019-01-01T12:15:20") == datetime.datetime(
            2019, 1, 1, 12, 15, 20
        )

    assert parse_datetime(
        "01/01/2023 12:15:20", format_="%d/%m/%Y %H:%M:%S"
    ) == datetime.datetime(2023, 1, 1, 12, 15, 20)


def test_str_to_date():
    from endi.utils.datetimes import str_to_date

    assert str_to_date("12/11/2014") == datetime.datetime(2014, 11, 12)
    assert str_to_date("12/11/14") == datetime.datetime(2014, 11, 12)
    assert str_to_date("12-11-2014") == datetime.datetime(2014, 11, 12)
    assert str_to_date("20121114") == datetime.datetime(2012, 11, 14)
    assert str_to_date(None) == None
    assert str_to_date("12/11/14", formats=("%y/%m/%d",)) == datetime.datetime(
        2012, 11, 14
    )


def test_format_duration():
    from endi.utils.datetimes import format_duration

    assert format_duration((12, 12)) == "12h12"
    assert format_duration((12, 00)) == "12h"
    assert format_duration((12, 00), short=False) == "12h00"


def test_datetools():
    from endi.utils.datetimes import DateTools

    dt = DateTools()
    assert dt.year_start(2023) == datetime.date(2023, 1, 1)
    assert dt.year_end(2023) == datetime.date(2023, 12, 31)
    assert dt.month_start(2023, 6) == datetime.date(2023, 6, 1)
    assert dt.month_end(2023, 6) == datetime.date(2023, 6, 30)
    assert dt.month_end(2024, 2) == datetime.date(2024, 2, 29)
    assert dt.previous_year_start(2023) == datetime.date(2022, 1, 1)
    assert dt.previous_year_end(2023) == datetime.date(2022, 12, 31)
    assert dt.previous_month_start(2023, 6) == datetime.date(2023, 5, 1)
    assert dt.previous_month_end(2023, 6) == datetime.date(2023, 5, 31)
    assert dt.previous_month_end(2024, 3) == datetime.date(2024, 2, 29)
    assert dt.format_date(datetime.date(2023, 6, 15)) == "15/06/2023"
    assert dt.format_date(datetime.date(2023, 6, 15), True) == "15 juin 2023"
    assert (
        dt.format_date(datetime.datetime(2023, 6, 15, 12, 30, 45)) == "15/06/2023 12:30"
    )
    assert (
        dt.format_date(datetime.datetime(2023, 6, 15, 12, 30, 45), True, True)
        == "15 juin 2023"
    )
    assert dt.format_date(1686825004) == "15/06/2023 12:30"
    assert dt.format_date(1686825004, True, True) == "15 juin 2023"
    with pytest.raises(ValueError):
        dt.format_date("2023 06 15")
    assert dt.format_date("20230615") == "15/06/2023"
    assert dt.format_date("2023-06-15", True, False) == "15 juin 2023"
    assert dt.format_date("15/06/2023", True) == "15 juin 2023"
