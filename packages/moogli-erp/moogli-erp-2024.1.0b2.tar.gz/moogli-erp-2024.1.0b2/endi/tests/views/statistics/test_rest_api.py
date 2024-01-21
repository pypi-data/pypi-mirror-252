import pytest
from endi.models import statistics as models
from endi.views.statistics.rest_api import RestStatisticEntry, RestStatisticCriterion


@pytest.fixture
def sheet(dbsession):
    sheet = models.StatisticSheet(title="test_sheet")
    dbsession.add(sheet)
    dbsession.flush()
    return sheet


@pytest.fixture
def full_sheet(dbsession, sheet):
    entry = models.StatisticEntry(
        title="test_entry",
        description="test entry",
        sheet_id=sheet.id,
    )
    dbsession.add(entry)
    dbsession.flush()
    top_level = models.StatisticCriterion(type="and", entry_id=entry.id)
    dbsession.add(top_level)
    dbsession.flush()

    criterion_1 = models.StatisticCriterion(
        type="boolean",
        key="parcours_num_hours",
        method="eq",
        search1=20,
        entry_id=entry.id,
        parent_id=top_level.id,
    )
    criterion_2 = models.StatisticCriterion(
        type="onetomany",
        key="career_path",
        entry_id=entry.id,
        parent_id=top_level.id,
    )
    dbsession.add(criterion_1)
    dbsession.add(criterion_2)
    dbsession.flush()

    criterion_21 = models.StatisticCriterion(
        key="start_date",
        method="this_year",
        entry_id=entry.id,
        parent_id=criterion_2.id,
    )
    criterion_22 = models.StatisticCriterion(
        type="string",
        key="stage_type",
        method="eq",
        search1="entry",
        entry_id=entry.id,
        parent_id=criterion_2.id,
    )
    dbsession.add(criterion_21)
    dbsession.add(criterion_22)
    dbsession.flush()
    return sheet


def test_rest_entry_add(full_sheet, get_csrf_request_with_db):
    appstruct = {
        "title": "Nouvelle entrée",
        "description": "Description",
    }
    request = get_csrf_request_with_db()
    request.context = full_sheet
    request.json_body = appstruct
    view = RestStatisticEntry(request)
    view.post()

    entry = full_sheet.entries[1]
    assert entry.title == "Nouvelle entrée"
    assert entry.description == "Description"
    # Auto add of AND criteria as top level
    assert len(entry.criteria) == 1


def test_rest_entry_edit(full_sheet, get_csrf_request_with_db):
    appstruct = {
        "title": "Entrée éditée",
    }
    request = get_csrf_request_with_db()
    request.context = full_sheet.entries[0]
    request.json_body = appstruct
    view = RestStatisticEntry(request)
    view.put()

    entry = full_sheet.entries[0]
    assert entry.title == "Entrée éditée"
    assert entry.description == "test entry"


class TestRestStatisticCriterion:
    def test_add_to_base(self, full_sheet, get_csrf_request_with_db):
        appstruct = {
            "key": "coordonnees_lastname",
            "parent_id": full_sheet.entries[0].criteria[0].id,
            "type": "string",
        }
        request = get_csrf_request_with_db()
        request.context = full_sheet.entries[0]
        request.json_body = appstruct
        view = RestStatisticCriterion(request)
        res = view.post()

        entry = full_sheet.entries[0]
        assert len(entry.criteria[0].children) == 3
        assert res.type == "string"
        assert res.key == "coordonnees_lastname"

    def test_add_to_non_complex_criterion(self, full_sheet, get_csrf_request_with_db):
        criterion_1 = full_sheet.entries[0].criteria[0].children[0]
        appstruct = {
            "key": "coordonnees_lastname",
            "parent_id": criterion_1.id,
            "type": "string",
        }
        request = get_csrf_request_with_db()
        request.context = full_sheet.entries[0]
        request.json_body = appstruct
        view = RestStatisticCriterion(request)
        new_criterion = view.post()

        assert new_criterion.parent.type == "and"
        assert new_criterion.parent.children[0] == criterion_1

        entry = full_sheet.entries[0]
        assert len(entry.criteria[0].children) == 2

    def test_add_to_o2m_criterion(self, full_sheet, get_csrf_request_with_db):
        criterion_2 = full_sheet.entries[0].criteria[0].children[1]
        appstruct = {
            "key": "end_date",
            "parent_id": criterion_2.id,
            "type": "date",
        }
        request = get_csrf_request_with_db()
        request.context = full_sheet.entries[0]
        request.json_body = appstruct
        view = RestStatisticCriterion(request)
        new_criterion = view.post()

        assert new_criterion.parent == criterion_2

        assert len(criterion_2.children) == 3
