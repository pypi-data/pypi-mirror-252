from endi.utils.menu import (
    BaseMenuElement,
    BaseAppMenuContainer,
    AppMenuItem,
    HtmlAppMenuItem,
    AppMenu,
    AppMenuDropDown,
)
from endi.tests.tools import (
    DummyRoute,
    set_route,
)


class TestBaseMenuElement:
    def test__is_deferred_property(self):
        elem = BaseMenuElement()
        assert not elem._is_deferred_property("test")
        elem.test = "1"
        assert not elem._is_deferred_property("test")
        elem.test = lambda menu: "1"
        assert elem._is_deferred_property("test")

    def test__get_deferred_property(self):
        elem = BaseMenuElement()
        assert elem._get_deferred_property("test") is None
        elem.test = "test"
        assert elem._get_deferred_property("test") == "test"

        elem.test = lambda menu, kw: kw["a"]
        assert elem._get_deferred_property("test", a=5) == 5

        elem.bind(a=6)
        assert elem._get_deferred_property("test") == 6

    def test_allowed(self, config, pyramid_request):
        elem = BaseMenuElement()
        assert elem.allowed(None)
        config.testing_securitypolicy(userid="login", permissive=False)
        elem.permission = "manage"
        assert not elem.allowed(pyramid_request)

        config.testing_securitypolicy(userid="login", permissive=True)
        elem.permission = "manage"
        assert elem.allowed(pyramid_request)

        config.testing_securitypolicy(userid="login", permissive=False)
        elem.permission = None
        elem.not_permission = "manage"
        assert elem.allowed(pyramid_request)

        config.testing_securitypolicy(userid="login", permissive=True)
        assert not elem.allowed(pyramid_request)

        elem.not_permission = None
        elem.permission = lambda menu, kw: kw["a"]
        elem.bind(a=True)
        assert elem.allowed(pyramid_request)

        elem.bind(a=False)
        assert not elem.allowed(pyramid_request)


class TestAppMenuItem:
    def test_item(self, pyramid_request, config):
        config.add_route("/a", "/a")
        config.add_route("/b", "/b")
        config.add_route("/b", "/b")
        config.add_route("/c", "/c")
        config.add_route("/a/{id}", "/a/{id}")
        config.add_route("/z/{id}", "/z/{id}")

        i1 = AppMenuItem(label="", icon="", href="/a")
        i2 = AppMenuItem(label="", icon="", href="/b")
        i3 = AppMenuItem(label="", icon="", href="/c", routes_prefixes=["/a"])

        set_route(pyramid_request, "/a")

        assert i1.selected(pyramid_request, i1.href)
        assert not i2.selected(pyramid_request, i2.href)
        assert i3.selected(pyramid_request, i3.href)

        set_route(pyramid_request, "/a/12", "/a/{id}")

        assert not i1.selected(pyramid_request, i1.href)
        assert not i2.selected(pyramid_request, i2.href)
        assert i3.selected(pyramid_request, i3.href)

        set_route(pyramid_request, "/z/12", "/z/{id}")

        assert not i1.selected(pyramid_request, i1.href)
        assert not i2.selected(pyramid_request, i2.href)
        assert not i3.selected(pyramid_request, i3.href)


class TestBaseAppMenuContainer:
    def test_add(self):
        container = BaseAppMenuContainer()
        container.add(AppMenuItem(label="test", order=2, href="/test"))
        container.add(AppMenuItem(label="test2", order=1, href="/test2"))
        item_no_order = AppMenuItem(label="test3", href="/test2")
        container.add(item_no_order)
        assert len(container.items) == 3
        assert container.items[0].label == "test2"
        assert item_no_order.order == 2

    def test_addsubnode(self):
        container = BaseAppMenuContainer()

        container.add(AppMenuDropDown(label="test", order=2, name="test"))
        container.add(
            AppMenuItem(label="test2", order=1, href="/test2"),
            "test",
        )

        container.add(AppMenuItem(label="test3", order=0, href="/test3"))
        assert len(container.items) == 2
        assert container.items[0].label == "test3"
        assert container.items[1].items[0].label == "test2"


class TestAppMenu:
    def test_build(self, pyramid_request):
        menu = AppMenu()
        menu.add(AppMenuDropDown(label="testdd", name="testdd"))
        menu.add(AppMenuItem(label="test", href="/test"), "testdd")

        # Not visible because perm is False
        menu.add(
            AppMenuDropDown(
                label="testdd", name="testdd2", permission=lambda _, kw: False
            )
        )
        menu.add(AppMenuItem(label="test", href="/test"), "testdd2")

        # Not visible because no item
        menu.add(
            AppMenuDropDown(
                label="testdd",
                name="testdd3",
            )
        )
        menu.add(
            AppMenuItem(label="test", permission=lambda _, kw: False, href="/test"),
            "testdd2",
        )
        set_route(pyramid_request, "/other")
        res = menu.build(pyramid_request)
        assert res == {
            "__type__": "menu",
            "items": [
                {
                    "__type__": "dropdown",
                    "label": "testdd",
                    "icon": None,
                    "items": [
                        {
                            "__type__": "item",
                            "label": "test",
                            "href": "/test",
                            "icon": None,
                            "selected": False,
                        }
                    ],
                }
            ],
        }
