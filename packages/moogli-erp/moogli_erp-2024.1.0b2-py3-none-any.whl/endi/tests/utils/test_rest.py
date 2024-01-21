from endi.utils.rest import (
    RestJsonRepr,
    RestError,
)


class DummyModel(dict):
    def appstruct(self):
        return self


class DummySchema:
    def serialize(self, datadict):
        return {"schemakey": datadict["schemakey"] * 2}

    def bind(self, **params):
        self.bind_params = params
        return self


class DummyJsonRepr(RestJsonRepr):
    schema = DummySchema()


def test_json():
    datas = DummyModel(schemakey=10, otherkey="dummy")
    jsonrepr = DummyJsonRepr(datas)
    assert set(jsonrepr.__json__("request").keys()).difference(
        list(datas.keys())
    ) == set([])


def test_bind_params():
    jsonrepr = DummyJsonRepr({}, bind_params=dict(test=5))
    schema = jsonrepr.get_schema("request")
    assert list(schema.bind_params.keys()) == ["test"]
    jsonrepr = DummyJsonRepr({})
    schema = jsonrepr.get_schema("request")
    assert list(schema.bind_params.keys()) == ["request"]


def test_it(config):
    err = RestError({}, 151)
    assert err.status == "151 Continue"
    assert err.content_type == "application/json"


def test_script_utils():
    from endi.scripts.utils import get_value

    args = {"--test": "toto", "--": "titi"}
    assert get_value(args, "test", "") == "toto"
    assert get_value(args, "test1", "test") == "test"
