from endi.models.form_options import FormFieldDefinition


def test_get_definitions(dbsession, mk_form_field_definition):
    field_def = mk_form_field_definition(field_name="test", form="test", title="Test")
    res = FormFieldDefinition.get_definitions("test")
    assert res.count() == 1
    res = FormFieldDefinition.get_definitions("other")
    assert res.count() == 0
    res = FormFieldDefinition.get_definition("test", "test")
    assert res == field_def

    field_def.visible = False
    dbsession.merge(field_def)
    dbsession.flush()
    res = FormFieldDefinition.get_definitions("test")
    assert res.count() == 0


def test_form_config(dbsession, mk_form_field_definition):
    field_def = mk_form_field_definition(
        field_name="test", form="test", title="Test", required=True
    )
    res = field_def.form_config()["test"]
    assert res["title"] == "Test"
    assert res["required"]
    assert res["edit"]
    field_def.required = False

    res = field_def.form_config()["test"]
    assert not res["required"]


def test_get_form_labels(mk_form_field_definition):
    mk_form_field_definition(
        field_name="test", form="test", title="Test", required=True
    )
    assert FormFieldDefinition.get_form_labels("test") == {"test": "Test"}
