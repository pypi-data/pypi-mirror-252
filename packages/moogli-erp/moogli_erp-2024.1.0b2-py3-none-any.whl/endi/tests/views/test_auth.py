"""
    Tests
"""
from unittest.mock import MagicMock


def test_redirect(app):
    login_url = "http://localhost/login?nextpage=%2F"
    resp = app.get("/")
    assert resp.status_int == 302
    assert login_url in list(dict(resp.headerlist).values())


def test_xhr_redirect(app):
    login_url = "http://localhost/login?nextpage=%2F"
    resp = app.get("/", xhr=True)
    assert resp.status_int == 200
    assert resp.json["redirect"] == login_url


def test_check_login(app, config):
    login_url = "http://localhost/api/v1/login"
    resp = app.get(login_url, xhr=True)
    assert resp.json["status"] == "error"
    assert "login_form" in resp.json["datas"]


# def get_avatar():
#    user = MagicMock(name='test', companies=[])
#    user.companies = [MagicMock(name='Test', id=100), MagicMock(name='Test2', id=101)]
#    return user
#
#
# def get_avatar2():
#    user = MagicMock(name='test2')
#    user.companies = [MagicMock(name='Test', id=100)]
#    return user
#
#
# def test_index_view(config, get_csrf_request):
#    from endi.views.index import index
#    config.add_route('company', '/company/{id}')
#    config.add_route('manage', '/manage/')
#    config.add_static_view('static', 'endi:static')
#    request = get_csrf_request()
#    avatar = get_avatar()
#    request._user = avatar
#    request.identity = avatar
#    response = index(request)
#    assert avatar.companies == response['companies']
#    avatar = get_avatar2()
#    request._user = avatar
#    request.identity = avatar
#    response = index(request)
#    assert response.status_int == 302
