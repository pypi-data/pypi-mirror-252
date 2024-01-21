import pytest
import colander
from pyramid import testing


def test_password_change_schema(user, user2, mk_login, config, pyramid_request):
    from endi.forms.user.login import get_password_schema

    schema = get_password_schema()
    pyramid_request.context = mk_login(login="second login", login_user=user2)
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize({"pwd_hash": "New pass"})

    assert result["pwd_hash"] == "New pass"


def test_mypassword_change_schema(login, user, config, pyramid_request):
    from endi.forms.user.login import get_password_schema

    schema = get_password_schema()
    pyramid_request.context = login
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))

    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize({"password": "pwd", "pwd_hash": "New pass"})

    assert result["pwd_hash"] == "New pass"

    with pytest.raises(colander.Invalid):
        schema.deserialize({"password": "ooo", "pwd_hash": "New pass"})


def test_add_schema(dbsession, pyramid_request, login, groups):

    from endi.forms.user.login import get_add_edit_schema

    schema = get_add_edit_schema()
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            "login": "test2",
            "pwd_hash": "oo",
            "primary_group": "contractor",
            "groups": ["trainer"],
            "user_id": 1500,
        }
    )

    assert "pwd_hash" in result

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "",
                "primary_group": "contractor",
                "groups": ["trainer"],
                "user_id": 1500,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "login",
                "pwd_hash": "ooo",
                "primary_group": "contractor",
                "groups": ["trainer"],
                "user_id": 1500,
            }
        )
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "ooo",
                "primary_group": "",
                "groups": ["trainer"],
                "user_id": 1500,
            }
        )


def test_edit_schema_login_context(dbsession, pyramid_request, login, user, groups):

    from endi.forms.user.login import get_add_edit_schema
    from endi.models.user.login import Login
    from endi.models.user.user import User

    user2 = User(email="a@a.fr", lastname="lastname2", firstname="firstname2")
    dbsession.add(user2)
    dbsession.flush()

    item = Login(user_id=user2.id, login="test2")
    item.set_password("pwd2")
    dbsession.add(item)
    dbsession.flush()

    pyramid_request.context = item

    schema = get_add_edit_schema(edit=True)
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            "login": "test2",
            "pwd_hash": "",
            "primary_group": "manager",
            "groups": ["trainer"],
            "user_id": user2.id,
        }
    )

    assert "pwd_hash" not in result

    result = schema.deserialize(
        {
            "login": "test2",
            "pwd_hash": "notpwd2",
            "primary_group": "manager",
            "groups": ["trainer"],
            "user_id": user2.id,
        }
    )

    assert "pwd_hash" in result

    # Login already used
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "login",
                "pwd_hash": "",
                "primary_group": "manager",
                "groups": ["trainer"],
                "user_id": user2.id,
            }
        )

    # User already linked to Login class
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "ooo",
                "primary_group": "manager",
                "groups": ["trainer"],
                "user_id": user.id,
            }
        )

    # wrong primary group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "ooo",
                "primary_group": "falseone",
                "groups": ["trainer"],
                "user_id": user2.id,
            }
        )
    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "ooo",
                "primary_group": "contractor",
                "user_id": user2.id,
                "groups": ["falseone"],
            }
        )


def test_edit_schema_user_context(dbsession, pyramid_request, login, user, groups):

    from endi.forms.user.login import get_add_edit_schema
    from endi.models.user.login import Login
    from endi.models.user.user import User

    user2 = User(email="a@a.fr", lastname="lastname2", firstname="firstname2")
    dbsession.add(user2)
    dbsession.flush()

    item = Login(user_id=user2.id, login="test2")
    item.set_password("pwd2")
    dbsession.add(item)
    dbsession.flush()

    pyramid_request.context = user2

    schema = get_add_edit_schema(edit=True)
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            "login": "test2",
            "pwd_hash": "",
            "primary_group": "contractor",
            "groups": ["trainer"],
            "user_id": user2.id,
        }
    )

    assert "pwd_hash" not in result

    result = schema.deserialize(
        {
            "login": "test2",
            "pwd_hash": "notpwd2",
            "primary_group": "contractor",
            "groups": ["trainer"],
            "user_id": user2.id,
        }
    )

    assert "pwd_hash" in result

    # Login already used
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": login.login,
                "pwd_hash": "",
                "primary_group": "contractor",
                "user_id": user2.id,
                "groups": ["trainer"],
            }
        )

    # User already linked to Login class
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "",
                "primary_group": "contractor",
                "user_id": user.id,
            }
        )

    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "",
                "primary_group": "unknown group",
                "groups": ["trainer"],
                "user_id": user2.id,
            }
        )

    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "login": "test2",
                "pwd_hash": "",
                "primary_group": "contractor",
                "groups": ["unknown group"],
                "user_id": user2.id,
            }
        )


def test_auth_schema(dbsession, login):

    from endi.forms.user.login import get_auth_schema

    schema = get_auth_schema()
    result = schema.deserialize({"login": login.login, "password": "pwd"})
    assert "password" in result

    with pytest.raises(colander.Invalid):
        schema.deserialize({"login": "nottest", "password": "pwd"})

    with pytest.raises(colander.Invalid):
        schema.deserialize({"login": "login", "password": "notpwd"})
