import pytest
import colander
import datetime

from endi.plugins.sap_urssaf3p.models.customer import UrssafCustomerData


@pytest.fixture
def mk_urssaf_payment_request(fixture_factory, invoice):
    from endi.plugins.sap_urssaf3p.models.payment_request import URSSAFPaymentRequest

    return fixture_factory(
        URSSAFPaymentRequest,
        parent=invoice,
    )


@pytest.fixture
def urssaf_payment_request(mk_urssaf_payment_request):
    return mk_urssaf_payment_request()


@pytest.fixture
def mk_urssaf_customer_data(fixture_factory):
    return fixture_factory(
        UrssafCustomerData,
        client_id="6a56a628-b09e-8707-787e-10f218a2d550",
        street_type="R",
        street_name="du soleil",
        lieu_dit=colander.null,
        birth_name="Dupont",
        birthdate=datetime.date(1990, 1, 1),
        birthplace_city="Meulun",
        birthplace_city_code="77288",
        birthplace_country_code="99100",
        bank_account_bic="BNPAFRPP",
        bank_account_iban="FR7630004000031234567890143",
        bank_account_owner="Jean Dupont",
    )


@pytest.fixture
def sap_customer(mk_customer, mk_urssaf_customer_data):
    customer = mk_customer(
        civilite="Monsieur",
        lastname="Durand",
        firstname="?Éric-Antoine Jean alain?",
        address="8 rue du soleil",
        zip_code="26110",
        city="Nyons",
        mobile="0605040302",
        email="jeanne.durand@contact.fr",
        city_code="26220",
        country_code="99100",
        additional_address="Batiment A",
    )
    mk_urssaf_customer_data(customer=customer)
    return customer
