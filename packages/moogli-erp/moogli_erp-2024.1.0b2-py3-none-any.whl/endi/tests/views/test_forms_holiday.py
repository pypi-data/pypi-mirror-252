import datetime
import colander
import pytest

from endi.forms.holiday import date_validator, HolidaySchema


def test_date_validator():
    start_date = datetime.date(2012, 11, 1)
    end_date = datetime.date(2012, 11, 2)
    form = HolidaySchema()
    date_validator(form, {"start_date": start_date, "end_date": end_date})
    with pytest.raises(colander.Invalid):
        date_validator(form, {"start_date": end_date, "end_date": start_date})
