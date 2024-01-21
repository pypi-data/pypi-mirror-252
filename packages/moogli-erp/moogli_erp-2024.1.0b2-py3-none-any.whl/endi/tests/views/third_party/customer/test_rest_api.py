import pytest
from endi.utils.rest import RestError
from endi.models.third_party import Customer
from endi.views.third_party.customer.rest_api import CustomerRestView


COMPANY_APPSTRUCT = {
    "type": "company",
    "company_name": "Company",
    "lastname": "Lastname",
    "address": "Address",
    "zip_code": "21000",
    "city": "Dijon",
    "compte_cg": "Compte CG1515",
    "compte_tiers": "Compte Tiers",
    "code": "CODE",
    "registration": "SIRET0123",
}


INDIVIDUAL_APPSTRUCT = {
    "type": "individual",
    "lastname": "Lastname 2",
    "firstname": "FirstName",
    "address": "Address",
    "zip_code": "21000",
    "city": "Dijon",
    "compte_cg": "Compte CG1515",
    "compte_tiers": "Compte Tiers",
    "code": "CODE",
}


def get_customers_query(company):
    return Customer.query().filter(Customer.company_id == company.id)


class TestCustomerRestView:
    def test_get_customers(
        self,
        get_csrf_request_with_db,
        customer,
        company,
    ):
        request = get_csrf_request_with_db()
        request.context = company
        view = CustomerRestView(request)
        result = view.collection_get()
        assert len(result) == 1
        assert result[0]["company_name"] == customer.name

    def test_get_customers_other_company(
        self,
        dbsession,
        get_csrf_request_with_db,
        customer,
        company2,
    ):
        request = get_csrf_request_with_db()
        request.context = company2
        view = CustomerRestView(request)
        result = view.collection_get()
        assert len(result) == 0

    def test_post_company(self, get_csrf_request_with_db, company):
        appstruct = COMPANY_APPSTRUCT.copy()
        request = get_csrf_request_with_db(post=appstruct)
        request.context = company
        view = CustomerRestView(request)
        view.post()

        customer = (
            get_customers_query(company)
            .filter_by(company_name=COMPANY_APPSTRUCT["company_name"])
            .first()
        )
        for key, value in COMPANY_APPSTRUCT.items():
            assert getattr(customer, key) == value

    def test_post_individual(self, get_csrf_request_with_db, company):
        appstruct = INDIVIDUAL_APPSTRUCT.copy()
        request = get_csrf_request_with_db(post=appstruct)
        request.context = company
        view = CustomerRestView(request)
        view.post()

        customer = (
            get_customers_query(company)
            .filter_by(lastname=INDIVIDUAL_APPSTRUCT["lastname"])
            .first()
        )
        for key, value in INDIVIDUAL_APPSTRUCT.items():
            assert getattr(customer, key) == value

    def test_post_internal(self, get_csrf_request_with_db, company, company2):
        appstruct = {
            "type": "internal",
            "source_company_id": company2.id,
            "company_id": company.id,
        }
        request = get_csrf_request_with_db(post=appstruct)
        request.context = company
        view = CustomerRestView(request)
        view.post()

        customer = (
            get_customers_query(company).filter_by(company_name=company2.name).first()
        )
        assert customer.type == "internal"
        assert customer.email == "company2@c.fr"
        assert customer.source_company_id == company2.id

    def test_put_request(self, get_csrf_request_with_db, company, customer):
        request = get_csrf_request_with_db(
            post={"lastname": "Géorgio", "firstname": "Léonie"}
        )
        request.context = customer
        view = CustomerRestView(request)
        view.put()

        assert customer.lastname == "Géorgio"
        assert customer.firstname == "Léonie"
