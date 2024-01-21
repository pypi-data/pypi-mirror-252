from endi.tests.tools import Dummy


def test_add_user_submit_success(config, get_csrf_request_with_db):
    from endi.views.user.user import UserAddView
    from endi.models.user.user import User

    config.add_route("/users/{id}", "/users/{id}")

    appstruct = {
        "lastname": "Lastname 1",
        "firstname": "Firstname 1",
        "email": "a@example.com",
        "civilite": "Monsieur",
    }

    view = UserAddView(get_csrf_request_with_db())
    result = view.submit_success(appstruct)
    item = User.query().filter_by(lastname="Lastname 1").first()
    assert result.location == "/users/%s" % item.id


def test_add_user_submit_sucess_redirect_login(config, get_csrf_request_with_db):
    from endi.views.user.user import UserAddView
    from endi.models.user.user import User

    config.add_route("/users/{id}", "/users/{id}")
    config.add_route("/users/{id}/login/add", "/users/{id}/login/add")

    view = UserAddView(get_csrf_request_with_db())

    appstruct = {
        "lastname": "Lastname 1",
        "firstname": "Firstname 1",
        "email": "a@example.com",
        "civilite": "Monsieur",
        "add_login": "1",
    }
    result = view.submit_success(appstruct)
    item = User.query().filter_by(lastname="Lastname 1").first()
    assert result.location == "/users/%s/login/add" % item.id


def test_add_user_submit_success_confirm(user, config, get_csrf_request_with_db):
    from endi.views.user.user import UserAddView

    config.add_route("/users", "/users")
    config.add_route("/users/{id}", "/users/{id}")

    appstruct = {
        "lastname": user.lastname,
        "firstname": "Firstname 1",
        "email": "a@example.com",
        "civilite": "Monsieur",
    }
    req = get_csrf_request_with_db()
    req.matched_route = Dummy(name="/users")
    view = UserAddView(req)
    result = view.submit_success(appstruct)
    assert "duplicate_accounts" in result
    assert len(result["duplicate_accounts"]) == 1
    assert "form" in result


def test_edit_user_submit_success(user, config, get_csrf_request_with_db, dbsession):
    from endi.models.user.user import User
    from endi.views.user.user import UserEditView

    config.add_route("/users", "/users")
    config.add_route("/users/{id}", "/users/{id}")

    appstruct = {
        "lastname": user.lastname,
        "firstname": "new firstname",
        "email": "newadress@example.com",
        "civilite": "Monsieur",
    }
    req = get_csrf_request_with_db()
    req.context = user
    req.matched_route = Dummy(name="/users/{id}", id=user.id)
    req.matchdict = {"id": user.id}
    view = UserEditView(req)
    view.submit_success(appstruct)

    user = dbsession.query(User).filter_by(id=user.id).first()
    assert user.firstname == "new firstname"
    assert user.lastname == user.lastname
    assert user.email == "newadress@example.com"


def test_user_delete(user, config, get_csrf_request_with_db):
    from endi.views.user.user import UserDeleteView

    config.add_route("/users", "/users")
    req = get_csrf_request_with_db()
    req.context = user

    view = UserDeleteView(req)
    result = view.__call__()
    assert result.code == 302
    assert result.location == "/users"
