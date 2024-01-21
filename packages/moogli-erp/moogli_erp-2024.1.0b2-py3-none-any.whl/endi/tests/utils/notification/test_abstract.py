import datetime
import pytest

from endi.tests.tools import Dummy
from endi.utils.notification.abstract import AbstractNotification


class TestAbstractNotification:
    @pytest.fixture
    def abstract(self):
        return AbstractNotification(
            key="notification:key",
            title="Titre",
            body="Corps",
            check_query="select ...",
            due_datetime=(datetime.datetime.now() + datetime.timedelta(days=30)),
            context_tablename="table",
            context_id=15,
        )

    @pytest.fixture
    def dummy_event(self):
        return Dummy(
            key="notification:key",
            title="Titre",
            body="Corps",
            check_query="select ...",
            due_datetime=(datetime.datetime.now() + datetime.timedelta(days=30)),
            context_tablename="table",
            context_id=15,
        )

    def test_to_event(self, abstract):
        event = abstract.to_event()
        assert event.key == abstract.key
        assert event.title == abstract.title
        assert event.due_datetime == abstract.due_datetime
        assert event.context_tablename == abstract.context_tablename
        assert event.context_id == abstract.context_id

    def test_to_model(self, abstract, content):
        event = abstract.to_model()
        assert event.key == abstract.key
        assert event.title == abstract.title

    def test_from_event(self, dummy_event):
        abstract = AbstractNotification.from_event(dummy_event)
        for key in (
            "key",
            "title",
            "body",
            "check_query",
            "due_datetime",
            "context_tablename",
            "context_id",
        ):
            assert getattr(abstract, key) == getattr(dummy_event, key)
