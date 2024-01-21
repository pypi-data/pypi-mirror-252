import pytest
from endi.tests.tools import Dummy
from endi.models.third_party.services.customer import CustomerService


class TestCustomerService:
    def test_get_third_party_account(self, company3, company):
        assert (
            CustomerService.get_third_party_account(
                Dummy(compte_tiers="TEST", company=company3)
            )
            == "TEST"
        )

        assert (
            CustomerService.get_third_party_account(
                Dummy(compte_tiers="", company=company3)
            )
            == company3.third_party_customer_account
        )

        from endi.models.config import Config

        Config.set("cae_third_party_customer_account", "CAE1")
        assert (
            CustomerService.get_third_party_account(
                Dummy(compte_tiers=None, company=company)
            )
            == "CAE1"
        )

    def test_get_general_account(self, company3, company):
        assert (
            CustomerService.get_general_account(
                Dummy(compte_cg="TEST", company=company)
            )
            == "TEST"
        )
        assert (
            CustomerService.get_general_account(Dummy(compte_cg="", company=company3))
            == company3.general_customer_account
        )

        from endi.models.config import Config

        Config.set("cae_general_customer_account", "CAE1")
        assert (
            CustomerService.get_general_account(Dummy(compte_cg=None, company=company))
            == "CAE1"
        )
