import pytest

from endi.models.config import Config


def test_add_edit_schema(content, dbsession, pyramid_request):
    import colander
    from endi.forms.user.userdatas import get_add_edit_schema

    schema = get_add_edit_schema()
    schema.bind(request=pyramid_request)

    result = schema.deserialize(
        {
            "situation_situation_id": 1,
            "coordonnees_firstname": "firstname",
            "coordonnees_lastname": "lastname",
            "coordonnees_email1": "email1@email.fr",
        }
    )
    assert "coordonnees_firstname" in result

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "situation_situation_id": 1,
                "coordonnees_firstname": "firstname",
                "coordonnees_lastname": "lastname",
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "situation_situation_id": 1,
                "coordonnees_lastname": "lastname",
                "coordonnees_email1": "email1@email.fr",
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "situation_situation_id": 1,
                "coordonnees_firstname": "firstname",
                "coordonnees_email1": "email1@email.fr",
            }
        )

    # Userdatas custom fields
    assert "custom_fields" in schema
    assert len(schema["custom_fields"].children) == 0
    Config.set("userdatas_active_custom_fields", '["exp__diplome", "exp__competences"]')
    schema = get_add_edit_schema()
    assert "exp__diplome" in schema["custom_fields"]
    assert "exp__annee_diplome" not in schema["custom_fields"]
