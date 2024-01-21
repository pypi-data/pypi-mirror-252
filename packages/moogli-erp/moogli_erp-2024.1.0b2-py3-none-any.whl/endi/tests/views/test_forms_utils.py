import colander
from endi.views import BaseFormView


def test_init(get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    form = BaseFormView(req)
    assert form.dbsession == req.dbsession
    assert form.session == req.session


def test_more_vars_called(get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    form = BaseFormView(req)
    form.schema = DummySchema()
    form.add_template_vars = ("arg",)
    form.arg = "Test arg"
    result = form.__call__()
    assert result["arg"] == "Test arg"


class DummySchema(colander.MappingSchema):
    test = colander.SchemaNode(colander.String(), title="test")
