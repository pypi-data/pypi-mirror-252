def test_module_registry(config, pyramid_request):
    config.include("endi.utils.modules")
    from endi.utils.modules import _register_module, has_module

    _register_module(config, "endi.views.module")
    assert has_module(pyramid_request, "module")
    assert not has_module(pyramid_request, "other.module")
    _register_module(config, "other.module")
    assert has_module(pyramid_request, "other.module")


def test_plugin_registry(config, pyramid_request):
    config.include("endi.utils.modules")
    from endi.utils.modules import _register_plugin, has_plugin

    _register_plugin(config, "endi.plugins.plugin")
    assert has_plugin(pyramid_request, "plugin")
    assert not has_plugin(pyramid_request, "other.plugin")
    _register_plugin(config, "other.plugin")
    assert has_plugin(pyramid_request, "other.plugin")
