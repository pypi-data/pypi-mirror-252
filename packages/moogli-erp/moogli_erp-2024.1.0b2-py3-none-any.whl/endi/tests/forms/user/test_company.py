import pytest
import colander


def test_company_schema(company, pyramid_request):
    from endi.forms.user.company import get_company_association_schema

    schema = get_company_association_schema()
    schema = schema.bind(request=pyramid_request)

    assert schema.deserialize({"companies": [company.name]}) == {
        "companies": [company.name]
    }

    with pytest.raises(colander.Invalid):
        schema.deserialize({"companies": ["Wrong company"]})
