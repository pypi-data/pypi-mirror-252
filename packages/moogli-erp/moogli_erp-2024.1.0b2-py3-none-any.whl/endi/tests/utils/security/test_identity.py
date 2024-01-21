def test_avatar(dbsession, config, get_csrf_request, user, login):
    from endi.utils.security.identity import get_identity

    request = get_csrf_request()
    request.dbsession = dbsession
    avatar = get_identity(request, login.login)
    assert avatar.lastname == "Lastname"
