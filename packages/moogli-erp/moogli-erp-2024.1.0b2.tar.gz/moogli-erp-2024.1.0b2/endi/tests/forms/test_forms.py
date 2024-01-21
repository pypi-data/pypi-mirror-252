from unittest.mock import Mock

from endi.forms import (
    merge_session_with_post,
    flatten_appstruct,
    flatten_appstruct_to_key_value,
    truncate_preparer,
)


def test_merge_session_with_post():
    session = Mock()
    post = dict(id=12, name="Dupont", lastname="Jean", accounts=["admin", "user"])
    merge_session_with_post(session, post)
    assert session.name == "Dupont"
    assert "admin" in session.accounts


def test_flatten_appstruct():
    appstruct = {"key1": "value1", "key2": {"key3": "value3"}}
    assert flatten_appstruct(appstruct) == {"key1": "value1", "key3": "value3"}


def test_flatten_appstruct_to_key_value():
    appstruct = {
        "str": "string",
        "int": 42,
        "float": 4.2,
        "list": [1, 2, 4.2, "42"],
        "dict": {"a": 1, "b": 2.0, "c": "str"},
    }
    assert flatten_appstruct_to_key_value(appstruct) == {
        "str": "string",
        "int": 42,
        "float": 4.2,
        "list.0": 1,
        "list.1": 2,
        "list.2": 4.2,
        "list.3": "42",
        "dict.a": 1,
        "dict.b": 2.0,
        "dict.c": "str",
    }


def test_truncate_preparer():
    func = truncate_preparer(5)
    a = "123456789"
    assert func(a) == "12345"
