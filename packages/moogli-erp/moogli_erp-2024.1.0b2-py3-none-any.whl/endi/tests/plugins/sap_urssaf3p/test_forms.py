import pytest
from endi.forms.third_party.customer import CIVILITE_OPTIONS
from endi.models.third_party import Customer
from endi.plugins.sap_urssaf3p.models.customer import UrssafCustomerData
from endi.plugins.sap_urssaf3p.forms.customer import (
    get_urssaf_individual_customer_schema,
)
from copy import deepcopy

APPSTRUCT = {
    "type_": "individual",
    "civilite": "Monsieur",
    "lastname": "Famille",
    "firstname": "Prénom",
    "email": "mail@example.com",
    "mobile": "0602030405",
    "city": "Test",
    "city_code": "123456",
    "zip_code": "123456",
    "address": "15 rue adresse",
    "urssaf_data": {
        "street_name": "adresse",
        "street_type": "R",
        "birthdate": "2022-01-01",
        "birthplace_city": "dede",
        "birthplace_city_code": "",
        "birthplace_department_code": "",
        "birthplace_country_code": "99328",
        "bank_account_bic": "BDFEFRPPCCT",
        "bank_account_iban": "FR7630001007941234567890185",
        "bank_account_owner": "Tjebbes",
    },
}


def test_urssaf_customer_schema():
    schema = get_urssaf_individual_customer_schema()
    del schema["csrf_token"]
    test = deepcopy(APPSTRUCT)
    schema.deserialize(test)
    for key in (
        "firstname",
        "email",
        "mobile",
        "city",
        "city_code",
        "zip_code",
        "address",
    ):
        err = deepcopy(test)
        err.pop(key)
        with pytest.raises(Exception):
            schema.deserialize(err)

    for key in (
        "birthdate",
        "birthplace_city",
        "birthplace_country_code",
        "bank_account_bic",
        "bank_account_iban",
        "bank_account_owner",
        "street_type",
    ):
        err = deepcopy(test)
        err["urssaf_data"].pop(key)
        with pytest.raises(Exception):
            schema.deserialize(err)

    # Ref #3659
    err = deepcopy(test)
    err["mobile"] = "06 02 03 04 05"
    with pytest.raises(Exception):
        schema.deserialize(err)


def test_urssaf_customer_schema_objectify(sap_customer):
    schema = get_urssaf_individual_customer_schema()
    del schema["csrf_token"]

    appstruct = deepcopy(APPSTRUCT)
    appstruct["id"] = sap_customer.id
    data_id = sap_customer.urssaf_data.id
    appstruct["urssaf_data"]["id"] = data_id

    result = schema.objectify(appstruct, sap_customer)
    assert result.urssaf_data == sap_customer.urssaf_data
    assert result == sap_customer
    assert result.urssaf_data.id == data_id
