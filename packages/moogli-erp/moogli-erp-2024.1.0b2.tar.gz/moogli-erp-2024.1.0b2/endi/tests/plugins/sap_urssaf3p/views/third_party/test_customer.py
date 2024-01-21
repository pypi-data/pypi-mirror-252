import pytest
from copy import deepcopy
from endi.models.third_party import Customer
from endi.plugins.sap_urssaf3p.views.third_party.customer import (
    UrssafCustomerController,
    UrssafCustomerRestView,
)


pytestmark = [pytest.mark.plugin_sap_urssaf3p]


INDIVIDUAL_SAP_APPSTRUCT = {
    "type": "individual",
    "civilite": "Monsieur",
    "lastname": "Lastname 2",
    "firstname": "FirstName",
    "address": "12 rue de la Liberté",
    "zip_code": "21000",
    "city": "Dijon",
    "city_code": "21231",
    "compte_cg": "Compte CG1515",
    "compte_tiers": "Compte Tiers",
    "code": "CODE",
    "country": "FRANCE",
    "country_code": "99100",
    "email": "test@example.com",
    "mobile": "0611111111",
    "urssaf_data": {
        "street_type": "R",
        "street_name": "de la Liberté",
        "birth_name": "Lastname 3",
        "birthdate": "1979-12-12",
        "birthplace_city": "Briançon",
        "birthplace_city_code": "05023",
        "birthplace_department_code": "5",
        "birthplace_country_code": "99100",
        "bank_account_bic": "CCOPFRPPXXX",
        "bank_account_iban": "FR7642559000011234567890121",
        "bank_account_owner": "MR Lastname toto",
    },
}


def get_customers_query(company):
    return Customer.query().filter(Customer.company_id == company.id)


class TestUrssafCustomerController:
    def test_get_schema(self, get_csrf_request_with_db, company):
        pyramid_request = get_csrf_request_with_db(context=company)
        controller = UrssafCustomerController(pyramid_request)
        schema = controller.get_schema({"type": "individual", "urssaf_data": {}})
        assert "urssaf_data" in schema


class TestUrssafCustomerRestView:
    @pytest.fixture
    def view_factory(self, get_csrf_request_with_db):
        def _builder(context, appstruct):
            request = get_csrf_request_with_db(post=appstruct, context=context)
            return UrssafCustomerRestView(request)

        return _builder

    def test_post_individual(self, view_factory, company):
        appstruct = deepcopy(INDIVIDUAL_SAP_APPSTRUCT)
        view = view_factory(company, appstruct)
        view.post()

        customer = (
            get_customers_query(company)
            .filter_by(lastname=INDIVIDUAL_SAP_APPSTRUCT["lastname"])
            .first()
        )
        expected = deepcopy(INDIVIDUAL_SAP_APPSTRUCT)

        expected_urssaf_data = expected.pop("urssaf_data")
        for key, value in expected.items():
            assert getattr(customer, key) == value

        birth_date = expected_urssaf_data.pop("birthdate")
        urssaf_data = customer.urssaf_data
        for key, value in expected_urssaf_data.items():
            assert getattr(urssaf_data, key) == value
        import datetime

        assert urssaf_data.birthdate == (
            datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        )

    def test_put_individual(self, dbsession, view_factory, sap_customer):
        appstruct = deepcopy(INDIVIDUAL_SAP_APPSTRUCT)
        view = view_factory(sap_customer, appstruct)
        result = view.put()

        # Ref #3616 : suppression des données urssaf une fois sur deux
        assert "urssaf_data" in result

        appstruct.pop("urssaf_data")
        view = view_factory(sap_customer, appstruct)
        result = view.put()
        customer = dbsession.query(Customer).get(sap_customer.id)

        assert customer.urssaf_data is None
