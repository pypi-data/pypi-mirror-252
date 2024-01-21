from pyramid import testing
from endi.tests.tools import DummyForm
from endi.models.company import Company

DATAS = {
    "name": "Compané $& test",
    "goal": "Be the best",
    "contribution": "80",
    "submit": "submit",
    "logo": {},
    "header": {},
}


def test_company_dashboard(config, content, get_csrf_request_with_db, user, company):
    from endi.views.company.views import company_dashboard

    # Those are juste dependencies
    config.add_route("user_expenses", "user_expenses")
    from endi.views.third_party.customer.routes import COMPANY_CUSTOMERS_ROUTE

    config.add_route(COMPANY_CUSTOMERS_ROUTE, COMPANY_CUSTOMERS_ROUTE)

    config.add_route("/companies/{id}", "/companies/{cid}")
    config.add_static_view("static", "endi:static")
    request = get_csrf_request_with_db()
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))
    request.context = company
    response = company_dashboard(request)
    assert user.companies[0].name == response["company"].name


class TestCompanyAdd:
    def test_before(self, get_csrf_request_with_db):
        pyramid_request = get_csrf_request_with_db()
        pyramid_request.params["user_id"] = 1
        pyramid_request.referrer = "/test"
        from endi.views.company.views import CompanyAdd

        view = CompanyAdd(pyramid_request)
        form = DummyForm()
        view.before(form)
        assert form.appstruct["user_id"] == 1
        assert form.appstruct["come_from"] == "/test"

    def test_add(self, config, get_csrf_request_with_db):
        from endi.views.company.views import CompanyAdd

        config.add_route("/companies/{id}", "/companies/{id}")

        post = DATAS.copy()
        req = get_csrf_request_with_db(post=post)
        view = CompanyAdd(req)
        view.__call__()

        company = Company.query().filter_by(name="Compané $& test").first()
        assert company is not None
        assert company.goal == "Be the best"

    def test_come_from(self, config, get_csrf_request_with_db, user):
        from endi.views.company.views import CompanyAdd

        post = DATAS.copy()
        post["come_from"] = "/test"
        req = get_csrf_request_with_db(post=post)
        req.referrer = "/test"

        view = CompanyAdd(req)
        result = view.__call__()

        assert result.location == "/test"

        company = Company.query().filter_by(name="Compané $& test").first()
        assert company is not None
        assert company.goal == "Be the best"

    def test_user_id(self, config, get_csrf_request_with_db, user):
        from endi.views.company.views import CompanyAdd

        post = DATAS.copy()
        post["user_id"] = str(user.id)
        req = get_csrf_request_with_db(post=post)
        req.referrer = "/test"

        view = CompanyAdd(req)
        view.__call__()

        company = Company.query().filter_by(name="Compané $& test").first()
        assert company is not None
        assert user in company.employees

    def test_contribution_not_in_schema(
        self, config, get_csrf_request_with_db, mk_custom_invoice_book_entry_module
    ):
        from endi.views.company.views import CompanyAdd

        post = DATAS.copy()
        req = get_csrf_request_with_db(post=post)

        view = CompanyAdd(req)
        view.__call__()
        company = Company.query().filter_by(name="Compané $& test").first()
        assert company.contribution is None

    def test_contribution(
        self, config, get_csrf_request_with_db, mk_custom_invoice_book_entry_module
    ):
        from endi.views.company.views import CompanyAdd

        post = DATAS.copy()
        mk_custom_invoice_book_entry_module(name="contribution")
        req = get_csrf_request_with_db(post=post)
        view = CompanyAdd(req)
        view.__call__()
        company = Company.query().filter_by(name="Compané $& test").first()
        assert company is not None
        assert company.contribution == 80


class TestCompanyEdit:
    def test_edit(
        self,
        config,
        company,
        get_csrf_request_with_db,
        mk_custom_invoice_book_entry_module,
    ):
        mk_custom_invoice_book_entry_module(name="contribution")
        config.add_route("/companies/{id}", "/companies/{id}")
        from endi.views.company.views import CompanyEdit

        appstruct = DATAS.copy()
        appstruct["phone"] = "+33 0606060606"
        appstruct["contribution"] = "70"
        req = get_csrf_request_with_db(post=appstruct)
        req.context = company

        view = CompanyEdit(req)
        view.__call__()

        assert company.phone == "+33 0606060606"
        assert company.contribution == 70
        assert company.header_file is None


def test_company_disable_user_one_company(
    config, login, company, get_csrf_request_with_db
):
    from endi.views.company.views import CompanyDisableView

    config.add_route("/users/{id}/login", "/users/{id}/login")
    request = get_csrf_request_with_db(context=company)
    request.referrer = "company"
    view = CompanyDisableView(request)
    view()
    assert not company.active
    assert not login.active


def test_company_disable_user_more_companies(
    config, login, company, company2, get_csrf_request_with_db
):
    from endi.views.company.views import CompanyDisableView

    config.add_route("/users/{id}/login", "/users/{id}/login")
    request = get_csrf_request_with_db(context=company)
    request.referrer = "company"
    view = CompanyDisableView(request)
    view()
    assert not company.active
    # User also belongs to Other companies
    assert login.active
