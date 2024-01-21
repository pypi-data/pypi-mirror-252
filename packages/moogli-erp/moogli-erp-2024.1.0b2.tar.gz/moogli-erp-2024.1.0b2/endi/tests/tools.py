try:
    from pyramid.compat import is_nonstr_iter
except ModuleNotFoundError:
    from pyramid.util import is_nonstr_iter

from pyramid.authorization import (
    Allow,
    Everyone,
    ALL_PERMISSIONS,
)
from pyramid.interfaces import IRoutesMapper


class Dummy:
    def __init__(self, **kwargs):
        for key, value in list(kwargs.items()):
            setattr(self, key, value)


class DummyRoute(Dummy):
    pregenerator = None

    def generate(self, kw):
        self.kw = kw
        return self.result


class DummyRouteContext(Dummy):
    def get_route(self, route_name):
        return self.route


def set_route(pyramid_request, route_path, route_name=None):
    if route_name is None:
        route_name = route_path

    route = DummyRoute(name=route_name, result=route_path)
    mapper = DummyRouteContext(route=route)
    pyramid_request.matched_dict = {}
    pyramid_request.matched_route = route
    pyramid_request.registry.registerUtility(mapper, IRoutesMapper)


def check_acl(acl, permission, principals=()):
    """
    Test if the given acl list in the form
    ((Deny/Allow, <principals>, <permissions>),)

    Allow permission

    :param list acl: acl in the pyramid form
    :param permission: The permission to check, may also be an iterable of permissions.
    :param principals: If specified the principals to check for
    """
    if not is_nonstr_iter(principals):
        principals = [principals]

    if is_nonstr_iter(permission):
        results = {}
        for one_permission in permission:
            results[one_permission] = check_acl(acl, one_permission, principals)

        if len(set(results.values())) > 1:
            raise AssertionError(f"Not all asserted permissions are equal : {results}")
        else:
            return list(results.values())[0]

    for ace in acl:
        ace_action, ace_principal, ace_permissions = ace
        if ace_principal in principals or ace_principal == Everyone:
            if not is_nonstr_iter(ace_permissions):
                ace_permissions = [ace_permissions]
            if permission in ace_permissions or ALL_PERMISSIONS in ace_permissions:
                if ace_action == Allow:
                    return True
                else:
                    return False
    return False


class DummyForm:
    def __init__(self, *args, **kwargs):
        self.appstruct = None

    def set_appstruct(self, datas):
        self.appstruct = datas
