import pytest
from endi.tests.tools import DummyForm


class TestLoginAddView:
    def test_before(self, get_csrf_request_with_db, user):
        from endi.views.user.login import LoginAddView

        req = get_csrf_request_with_db()
        req.context = user

        view = LoginAddView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct["login"] == user.email
        assert form.appstruct["user_id"] == user.id
        assert form.appstruct["groups"] == []

    def test_before_groups(self, config, get_csrf_request_with_db, user):
        from endi.views.user.login import LoginAddView

        req = get_csrf_request_with_db()
        req.context = user
        req.session["user_form"] = {"defaults": {"groups": ["contractor"]}}

        view = LoginAddView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct["login"] == user.email
        assert form.appstruct["user_id"] == user.id
        assert form.appstruct["groups"] == ["contractor"]

    def test_submit_success(
        self,
        config,
        get_csrf_request_with_db,
        user,
        groups,
    ):
        from endi.views.user.login import LoginAddView
        from endi.models.user.login import Login

        config.add_route("/users/{id}", "/users/{id}")
        req = get_csrf_request_with_db()
        req.context = user

        appstruct = {
            "pwd_hash": "password",
            "login": "test1@email.fr",
            "primary_group": "contractor",
            "groups": ["trainer"],
        }

        view = LoginAddView(req)
        result = view.submit_success(appstruct)
        new_login = Login.query().filter_by(login="test1@email.fr").one()
        assert result.code == 302
        assert result.location == "/users/{0}".format(user.id)

        assert new_login.groups == ["trainer", "contractor"]
        assert new_login.auth("password")

    def test_submit_success_next_step(
        self,
        config,
        get_csrf_request_with_db,
        user,
        groups,
    ):
        from endi.views.user.login import LoginAddView
        from endi.models.user.login import Login

        config.add_route("/path1/{id}", "/path1/{id}")
        config.add_route("/path2/{id}", "/path2/{id}")
        req = get_csrf_request_with_db()
        req.context = user
        req.session["user_form"] = {"callback_urls": ["/path1/{id}", "/path2/{id}"]}

        appstruct = {"pwd_hash": "password", "login": "test1@email.fr"}

        view = LoginAddView(req)
        result = view.submit_success(appstruct)
        new_login = Login.query().filter_by(login="test1@email.fr").one()
        assert result.code == 302
        assert result.location == "/path2/{0}".format(user.id)
        assert req.session["user_form"]["callback_urls"] == ["/path1/{id}"]

        assert new_login.auth("password")


class TestLoginEditView:
    def test_before(self, get_csrf_request_with_db, user, groups, login):
        from endi.views.user.login import LoginEditView

        req = get_csrf_request_with_db()
        req.context = login
        login.invoice_limit_amount = 400.0

        view = LoginEditView(req)
        form = DummyForm()
        view.before(form)
        assert form.appstruct["login"] == login.login
        assert form.appstruct["user_id"] == user.id
        assert form.appstruct["invoice_limit_amount"] == 400.0

    def test_submit_success(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from endi.views.user.login import LoginEditView

        config.add_route("/users/{id}/login", "/users/{id}/login")

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            "pwd_hash": "new_password",
            "login": "test1@email.fr",
            "invoice_limit_amount": 200.0,
            "estimation_limit_amount": -100.0,
        }
        view = LoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(user.id)
        assert login.login == "test1@email.fr"
        assert login.invoice_limit_amount == 200.0
        assert login.estimation_limit_amount == 100.0
        assert login.auth("new_password")

    def test_submit_success_no_password(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from endi.views.user.login import LoginEditView

        config.add_route("/users/{id}/login", "/users/{id}/login")

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {"pwd_hash": "", "login": "test1@email.fr"}
        view = LoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(user.id)
        assert login.login == "test1@email.fr"

        assert login.auth("pwd")


class TestLoginPasswordView:
    def test_submit_success(self, config, get_csrf_request_with_db, login):
        from endi.views.user.login import LoginPasswordView

        config.add_route("/users/{id}/login", "/users/{id}/login")

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            "pwd_hash": "new_password",
        }
        view = LoginPasswordView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(login.user_id)
        assert login.auth("new_password")

    def test_submit_success_unchanged(self, config, get_csrf_request_with_db, login):
        from endi.views.user.login import LoginPasswordView

        config.add_route("/users/{id}/login", "/users/{id}/login")

        req = get_csrf_request_with_db()
        req.context = login

        appstruct = {
            "pwd_hash": "",
        }
        view = LoginPasswordView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(login.user_id)
        # Not changed
        assert login.auth("pwd")


class TestUserLoginEditView:
    def test_submit_success(
        self, config, get_csrf_request_with_db, user, groups, login
    ):
        from endi.views.user.login import UserLoginEditView

        config.add_route("/users/{id}/login", "/users/{id}/login")

        req = get_csrf_request_with_db()
        req.context = user

        appstruct = {
            "pwd_hash": "new_password",
            "login": "test1@email.fr",
            "primary_group": "manager",
            "groups": ["constructor", "trainer"],
        }
        view = UserLoginEditView(req)
        result = view.submit_success(appstruct)
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(login.user_id)
        assert login.login == "test1@email.fr"
        assert login.primary_group() == "manager"
        assert login.groups == ["constructor", "trainer", "manager"]


class TestLoginDisableView:
    def test_disable(self, config, login, get_csrf_request_with_db):
        from endi.views.user.login import LoginDisableView

        config.add_route("/users/{id}/login", "/users/{id}/login")
        req = get_csrf_request_with_db()
        req.context = login
        view = LoginDisableView(req)
        result = view()
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(login.user_id)
        assert not login.active
        # Now we reactivate again
        view()
        assert login.active

    def test_disable_with_company(
        self, config, login, company, get_csrf_request_with_db
    ):
        from endi.views.user.login import LoginDisableView

        config.add_route("/users/{id}/login", "/users/{id}/login")
        req = get_csrf_request_with_db()
        req.context = login
        view = LoginDisableView(req)
        result = view()
        assert result.code == 302
        assert result.location == "/users/{0}/login".format(login.user_id)
        assert not login.active
        assert not company.active
        # Now we reactivate again
        view()
        assert login.active


class TestLoginDeleteView:
    def test_delete(self, config, user, groups, login, get_csrf_request_with_db):
        from endi.views.user.login import LoginDeleteView
        from endi.models.user.login import Login

        config.add_route("/users/{id}", "/users/{id}")
        req = get_csrf_request_with_db()
        req.context = login

        login_id = login.id
        view = LoginDeleteView(req)
        result = view()
        assert result.code == 302
        assert result.location == "/users/{0}".format(user.id)
        req.dbsession.flush()
        assert Login.get(login_id) is None
