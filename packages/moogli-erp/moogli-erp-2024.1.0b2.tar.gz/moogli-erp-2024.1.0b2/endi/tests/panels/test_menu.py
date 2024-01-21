from pyramid import testing
from endi.tests.tools import (
    Dummy,
    DummyRoute,
)


def get_context(cid=200):
    context = Dummy()
    context.get_company_id = lambda: cid
    return context


def test_get_cid(get_csrf_request_with_db, dbsession, mk_user, mk_company):
    from endi.panels.menu import get_current_company

    user = mk_user(lastname="test", firstname="test")
    user2 = mk_user(lastname="test2", firstname="test2")
    company = mk_company("a", "b", "test", employee=user)
    company2 = mk_company("c", "d", "test", employee=user2)
    dbsession.merge(user)
    dbsession.flush()

    request = get_csrf_request_with_db(user=user)
    assert get_current_company(request).id == company.id
    assert request.current_company == company

    request.context = company2
    # reset du cache
    request.current_company = None
    assert get_current_company(request).id == company.id
    # reset du cache
    request.current_company = None
    assert get_current_company(request, submenu=True).id == company2.id


def test_get_companies(
    config, get_csrf_request_with_db, user, company, company2, dbsession
):
    from endi.panels.menu import get_companies

    config.set_security_policy(testing.DummySecurityPolicy(identity=user))
    request = get_csrf_request_with_db(user=user, context=get_context())

    user.companies = [company]
    dbsession.merge(user)
    dbsession.flush()
    config.testing_securitypolicy(userid="test", identity=user, permissive=False)
    assert get_companies(request, None) == request.identity.active_companies
    config.testing_securitypolicy(userid="test", identity=user, permissive=True)
    assert get_companies(request, company2) == [
        (company.id, "Company", "0USER", True, 1, "Lastname Firstname"),
        (company2.id, "Company2", "1USER", True, 0, None),
    ]
