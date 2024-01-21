"""
Test the csv import view module
"""
import pytest
from endi.views.csv_import import (
    get_preferences_obj,
    load_preferences,
    get_preference,
)


@pytest.fixture
def config(dbsession):
    from endi.models.config import Config

    c = Config(
        name="csv_import",
        value='{"test en action": {"PR\\u00e9nom": "coordonnees_firstname"}}',
    )
    dbsession.add(c)
    dbsession.flush()
    return c


def test_get_preferences_obj(config):
    assert get_preferences_obj().value is not None


def test_get_new_preference_obj():
    assert get_preferences_obj().value is None


def test_load_preferences(config):
    assert list(load_preferences(get_preferences_obj()).keys()) == ["test en action"]


def test_get_preference(config):
    assert get_preference("test en action") == {"PRénom": "coordonnees_firstname"}
