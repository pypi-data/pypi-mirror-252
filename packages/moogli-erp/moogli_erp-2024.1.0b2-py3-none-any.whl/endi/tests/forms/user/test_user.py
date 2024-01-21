import pytest
from endi.tests.tools import Dummy


def test_default_disable():
    from endi.forms.user.user import deferred_company_disable_default

    companies = [Dummy(employees=list(range(2)))]
    user = Dummy(companies=companies)
    req = Dummy(context=user)
    assert not deferred_company_disable_default("", {"request": req})
    companies = [Dummy(employees=[1])]
    user = Dummy(companies=companies)
    req = Dummy(context=user)
    assert deferred_company_disable_default("", {"request": req})


def test_user_add_schema(pyramid_request):
    import colander
    from endi.forms.user.user import get_add_edit_schema

    appstruct = {
        "civilite": "Monsieur",
        "lastname": "Test lastname",
        "firstname": "Firstname",
        "email": "a@a.fr",
        "add_login": "0",
        "photo_is_publishable": "0",
    }
    schema = get_add_edit_schema()
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize(appstruct)

    assert "email" in result
    # civilite
    with pytest.raises(colander.Invalid):
        appstruct = {
            "civilite": "Not a valid one",
            "lastname": "Test lastname",
            "firstname": "Firstname",
            "email": "a@a.fr",
            "add_login": "0",
            "photo_is_publishable": "0",
        }
        schema.deserialize(appstruct)
    # lastname
    with pytest.raises(colander.Invalid):
        appstruct = {
            "civilite": "Monsieur",
            "firstname": "Firstname",
            "email": "a@a.fr",
            "add_login": "0",
            "photo_is_publishable": "0",
        }
        schema.deserialize(appstruct)
    # firstname
    with pytest.raises(colander.Invalid):
        appstruct = {
            "civilite": "Monsieur",
            "lastname": "Test lastname",
            "email": "a@a.fr",
            "add_login": "0",
            "photo_is_publishable": "0",
        }
        schema.deserialize(appstruct)
    # email
    with pytest.raises(colander.Invalid):
        appstruct = {
            "civilite": "Monsieur",
            "lastname": "Test lastname",
            "firstname": "Firstname",
            "add_login": "0",
            "photo_is_publishable": "0",
        }
        schema.deserialize(appstruct)
    with pytest.raises(colander.Invalid):
        appstruct = {
            "civilite": "Monsieur",
            "lastname": "Test lastname",
            "firstname": "Firstname",
            "email": "notanemail",
            "add_login": "0",
            "photo_is_publishable": "0",
        }
        schema.deserialize(appstruct)
