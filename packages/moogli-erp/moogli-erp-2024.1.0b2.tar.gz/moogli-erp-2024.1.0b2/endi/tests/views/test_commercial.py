"""
    Test the commercial handling module
"""
import pytest
from datetime import date
from unittest.mock import Mock
from endi.views.commercial import (
    compute_turnover_difference,
    compute_turnover_percent,
)
from endi.views.commercial import DisplayCommercialHandling
from endi.models.commercial import TurnoverProjection

APPSTRUCT = {"month": 11, "value": "1500", "comment": "Some comments go here"}


class DummyProjection:
    def __init__(self, value):
        self.value = value


def getOne():
    return TurnoverProjection.query().first()


@pytest.fixture
def proj(request, config, get_csrf_request_with_db, company):
    config.add_route("commercial_handling", "/")
    req = get_csrf_request_with_db()
    req.context = company
    # On utilise la docstring pour stocker des paramètres, c sal mais ça marche
    year = request.function.__doc__
    if year:
        req.GET = {"year": year}
    view = DisplayCommercialHandling(None, req)
    view.submit_success(APPSTRUCT)
    return getOne()


def test_compute_turnover_difference():
    index = 0
    projections = {}
    turnovers = {}
    assert compute_turnover_difference(index, projections, turnovers) is None
    p = Mock(value=10)
    projections = {0: p}
    turnovers = {0: 10}
    assert compute_turnover_difference(1, projections, turnovers) is None
    assert 0 == compute_turnover_difference(0, projections, turnovers)


def test_submit_year(get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    req.GET = {"year": "2010"}
    view = DisplayCommercialHandling(None, req)
    assert view.submit_year() == {"year": 2010}
    req.GET = {}
    assert view.submit_year() == {"year": date.today().year}


def test_add(proj):
    assert int(proj.value) == 1500
    assert proj.comment == "Some comments go here"
    assert int(proj.year) == date.today().year


def test_add_with_year(proj):
    """2002"""
    assert int(proj.value) == 1500
    assert proj.comment == "Some comments go here"
    assert int(proj.year) == 2002


def test_edit(proj, get_csrf_request_with_db):
    appstruct = APPSTRUCT.copy()
    appstruct["value"] = 10
    req = get_csrf_request_with_db()
    view = DisplayCommercialHandling(None, req)
    view.submit_success(appstruct)
    proj = getOne()
    assert proj.value == 10


def test_compute_turnover_percent():
    proj = DummyProjection(0)
    assert compute_turnover_percent(0, {0: proj}, {0: 50}) == 0
    proj = DummyProjection(100)
    assert compute_turnover_percent(0, {0: proj}, {0: 50}) == 50.0


def test_get_range():
    from endi.views.commercial import (
        get_year_range,
        get_month_range,
    )
    import datetime

    assert get_year_range(2012) == (
        datetime.date(2012, 1, 1),
        datetime.date(2013, 1, 1),
    )
    assert get_month_range(3, 2012) == (
        datetime.date(2012, 3, 1),
        datetime.date(2012, 4, 1),
    )
    assert get_month_range(12, 2012) == (
        datetime.date(2012, 12, 1),
        datetime.date(2013, 1, 1),
    )
