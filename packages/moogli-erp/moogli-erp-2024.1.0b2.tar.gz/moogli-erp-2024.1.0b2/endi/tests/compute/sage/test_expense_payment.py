import pytest
import datetime
from unittest.mock import MagicMock
from endi.compute.sage.expense_payment import (
    SageExpensePaymentMain,
    SageExpensePaymentWaiver,
)
from endi.tests.tools import Dummy


@pytest.fixture
def expense():
    company = MagicMock(
        code_compta="COMP_ANA",
    )
    company.get_general_expense_account.return_value = "CGNDF"
    user = MagicMock(
        firstname="firstname",
        lastname="lastname",
        compte_tiers="COMP_TIERS",
    )

    return MagicMock(
        id=1254,
        company=company,
        user=user,
        month=5,
        year=2014,
        date=datetime.date.today(),
        official_number="official_number",
    )


@pytest.fixture
def expense_payment(expense, bank):
    p = Dummy(
        amount=10000000,
        mode="chèque",
        date=datetime.datetime.now(),
        expense=expense,
        bank=bank,
    )
    return p


@pytest.fixture
def sage_expense_payment(config_request, expense_payment):
    factory = SageExpensePaymentMain(None, config_request)
    factory.set_payment(expense_payment)
    return factory


@pytest.fixture
def sage_expense_payment_waiver(config_request, expense_payment):
    factory = SageExpensePaymentWaiver(None, config_request)
    factory.set_payment(expense_payment)
    return factory


@pytest.mark.payment
class TestSageExpensePaymentMain:
    def test_base_entry(self, sage_expense_payment):
        today = datetime.date.today()
        assert sage_expense_payment.reference == "official_number"
        assert sage_expense_payment.code_journal == "CODE_JOURNAL_BANK"
        assert sage_expense_payment.date == today
        assert sage_expense_payment.mode == "chèque"
        libelle = "LASTNAME / REMB FRAIS mai/2014"
        assert sage_expense_payment.libelle == libelle
        assert sage_expense_payment.code_taxe == "TVANDF"
        assert sage_expense_payment.num_analytique == "COMP_ANA"

    def test_credit_bank(self, sage_expense_payment):
        g_entry, entry = sage_expense_payment.credit_bank(10000000)
        assert entry["compte_cg"] == "COMPTE_CG_BANK"
        assert entry.get("compte_tiers", "") == ""
        assert entry["credit"] == 10000000

    def test_debit_entrepreneur(self, sage_expense_payment):
        g_entry, entry = sage_expense_payment.debit_user(10000000)
        assert entry["compte_cg"] == "CGNDF"
        assert entry["compte_tiers"] == "COMP_TIERS"
        assert entry["debit"] == 10000000


@pytest.mark.payment
class TestSageExpensePaymentWaiver:
    def test_code_journal(self, sage_expense_payment_waiver):
        assert sage_expense_payment_waiver.code_journal == "JOURNAL_ABANDON"

    def test_base_entry(self, sage_expense_payment_waiver):
        today = datetime.date.today()
        assert sage_expense_payment_waiver.reference == "official_number"
        assert sage_expense_payment_waiver.code_journal == "JOURNAL_ABANDON"
        assert sage_expense_payment_waiver.date == today
        assert sage_expense_payment_waiver.mode == "Abandon de créance"
        libelle = "Abandon de créance LASTNAME mai/2014"
        assert sage_expense_payment_waiver.libelle == libelle
        assert sage_expense_payment_waiver.code_taxe == ""
        assert sage_expense_payment_waiver.num_analytique == "COMP_ANA"

    def test_credit_bank(self, sage_expense_payment_waiver):
        g_entry, entry = sage_expense_payment_waiver.credit_bank(10000000)
        assert entry["compte_cg"] == "COMPTE_CG_WAIVER"
        assert entry.get("compte_tiers", "") == ""
        assert entry["credit"] == 10000000

    def test_debit_entrepreneur(self, sage_expense_payment_waiver):
        g_entry, entry = sage_expense_payment_waiver.debit_user(10000000)
        assert entry["compte_cg"] == "CGNDF"
        assert entry["compte_tiers"] == "COMP_TIERS"
        assert entry["debit"] == 10000000
