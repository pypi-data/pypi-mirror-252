from endi.utils.session import get_session_factory
from pyramid_beaker.tests import TestPyramidBeakerSessionObject
from pyramid import testing


class TestSession(TestPyramidBeakerSessionObject):
    def test_longtimeout(self):
        settings = {"session.longtimeout": 350, "session.timeout": 35}
        sessionfactory = get_session_factory(settings)
        request = testing.DummyRequest(cookies={"remember_me": "ok"})
        session = sessionfactory(request)
        assert session.timeout == 350

    def test_notlongtimeout(self):
        settings = {"session.longtimeout": 350, "session.timeout": 35}
        sessionfactory = get_session_factory(settings)
        request = testing.DummyRequest()
        session = sessionfactory(request)
        assert session.timeout == 35
