import time
import pytest
from hashlib import md5
from endi.tests.tools import Dummy
from pyramid.testing import DummyRequest


def test_get_timestamp_from_request():
    from endi.utils.security.api_key_predicate import get_timestamp_from_request

    with pytest.raises(KeyError):
        get_timestamp_from_request(DummyRequest())

    request = DummyRequest(headers={"timestamp": "124545.152"})
    assert get_timestamp_from_request(request) == "124545.152"

    request = DummyRequest(headers={"Timestamp": "124545.152"})
    assert get_timestamp_from_request(request) == "124545.152"


def test_check_timestamp():
    from endi.utils.security.api_key_predicate import check_timestamp

    assert check_timestamp(time.time(), tolerance=2)
    assert not check_timestamp(time.time() - 3, tolerance=2)


def test_get_clientsecret_from_request():
    from endi.utils.security.api_key_predicate import get_clientsecret_from_request

    request = DummyRequest()
    with pytest.raises(KeyError):
        get_clientsecret_from_request(request)

    with pytest.raises(ValueError):
        request = DummyRequest(headers={"authorization": "HMAC-OTHER secret"})
        get_clientsecret_from_request(request)

    with pytest.raises(KeyError):
        request = DummyRequest(headers={"authorization": "nospacesecret"})
        get_clientsecret_from_request(request)

    request = DummyRequest(headers={"authorization": "HMAC-MD5 secret"})
    assert get_clientsecret_from_request(request) == "secret"

    request = DummyRequest(headers={"authorization": "HMAC-MD5 secret"})
    assert get_clientsecret_from_request(request) == "secret"


def test_check_secret():
    from endi.utils.security.api_key_predicate import check_secret

    # In [8]: md5('123456-secret').hexdigest()
    # Out[8]: '06dda91136f6ad4688cdf6c8fd991696'
    assert check_secret("06dda91136f6ad4688cdf6c8fd991696", 123456, "secret")


def test_api_key_authentication():
    from endi.utils.security.api_key_predicate import ApiKeyAuthenticationPredicate

    request = DummyRequest(headers={"timestamp": time.time()})
    setattr(request, "registry", Dummy(settings={}))
    request.registry.settings["key"] = "secret"
    timestamp = request.headers["timestamp"]
    secret_str = "%s-secret" % timestamp
    secret_bstr = secret_str.encode("utf-8")
    request.headers["authorization"] = "HMAC-MD5 " + md5(secret_bstr).hexdigest()

    api = ApiKeyAuthenticationPredicate("key", None)
    assert api(None, request)

    api = ApiKeyAuthenticationPredicate("wrongkey", None)
    with pytest.raises(Exception):
        api(None, request)
