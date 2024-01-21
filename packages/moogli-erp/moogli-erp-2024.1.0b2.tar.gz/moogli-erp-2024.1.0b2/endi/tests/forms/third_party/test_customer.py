import colander
import pytest
from endi.tests.tools import Dummy


def test_company_customer_schema(pyramid_request):
    from endi.forms.third_party.customer import get_company_customer_schema

    schema = get_company_customer_schema()
    schema = schema.bind(request=pyramid_request)

    args = {
        "type": "company",
        "company_name": "Test customer",
        "civilite": "Monsieur",
        "address": "1 rue Victor Hugo",
        "lastname": "Lastname",
        "zip_code": "21000",
        "city": "Paris",
        "csrf_token": pyramid_request.session.get_csrf_token(),
        "registration": "123456ABC",
    }
    result = schema.deserialize(args)
    assert result["company_name"] == "Test customer"

    # mandatory fields
    for key in (
        "company_name",
        "registration",
    ):
        wrong = args.copy()
        wrong.pop(key)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)

    wrong = args.copy()
    wrong["email"] = "wrongmail"
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)

    wrong = args.copy()
    wrong["civilite"] = "wrongone"
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)


def test_individual_customer_schema(pyramid_request):
    from endi.forms.third_party.customer import get_individual_customer_schema

    schema = get_individual_customer_schema()
    schema = schema.bind(request=pyramid_request)
    args = {
        "type": "individual",
        "civilite": "M. et Mme",
        "address": "1 rue Victor Hugo",
        "lastname": "Lastname",
        "zip_code": "21000",
        "city": "Paris",
        "csrf_token": pyramid_request.session.get_csrf_token(),
    }
    result = schema.deserialize(args)
    assert result["lastname"] == "Lastname"

    # mandatory fields
    for field in ("lastname",):
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)


def test_internal_customer_addschema(company, company2):
    from endi.forms.third_party.customer import get_internal_customer_addschema

    schema = get_internal_customer_addschema()
    req = Dummy(context=company2)
    schema = schema.bind(request=req)

    args = {
        "type": "internal",
        "source_company_id": company.id,
        "company_id": company2.id,
    }
    result = schema.deserialize(args)
    assert result["source_company_id"] == company.id
    assert result["company_id"] == company2.id
    # mandatory fields
    wrong = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)

    customer = schema.objectify(result)
    assert customer.source_company_id == company.id
    assert customer.company_name == company.name
    assert customer.type == "internal"
    assert customer.company_id == company2.id
