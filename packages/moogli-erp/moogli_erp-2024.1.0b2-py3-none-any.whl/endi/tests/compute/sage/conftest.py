import pytest

from unittest.mock import MagicMock
from endi.compute.task import (
    LineCompute,
    GroupCompute,
)
from endi.compute.task.common import (
    InvoiceCompute,
)

from endi.models.task.payment import BankRemittance
from endi.tests.tools import Dummy


class DummyLine(Dummy, LineCompute):
    """
    Dummy line model
    """

    tva_object = None

    def get_tva(self):
        return self.tva_object


class DummyGroup(Dummy, GroupCompute):
    pass


class DummyInvoice(Dummy, InvoiceCompute):
    pass


class DummyRemittance(Dummy, BankRemittance):
    """
    Dummy bank remittance model
    """


@pytest.fixture
def config_request(pyramid_request, app_config, config):
    pyramid_request.config = app_config
    return pyramid_request


@pytest.fixture
def config_request_with_db(config_request, dbsession):
    config_request.dbsession = dbsession
    return config_request


@pytest.fixture
def dummy_tva_sans_code(mk_tva):
    return mk_tva(
        name="tva_sans_code",
        value=2000,
        default=0,
        compte_cg="TVA0001",
        compte_a_payer="TVAAPAYER0001",
        code=None,
    )


@pytest.fixture
def dummy_tva():
    return MagicMock(
        name="tva2", value=700, default=0, compte_cg="TVA0002", code="CTVA0002"
    )


@pytest.fixture
def dummy_tva10(mk_tva):
    return mk_tva(
        name="tva 10%", value=1000, default=0, compte_cg="TVA10", code="CTVA10"
    )


@pytest.fixture
def dummy_tva20(mk_tva):
    return mk_tva(
        name="tva 20%", value=2000, default=0, compte_cg="TVA20", code="CTVA20"
    )


@pytest.fixture
def def_dummy_tva(mk_tva):
    return mk_tva(
        name="tva1",
        value=1960,
        default=0,
        compte_cg="TVA0001",
        compte_a_payer="TVAAPAYER0001",
        code="CTVA0001",
    )


@pytest.fixture
def dummy_tva_computer(mk_tva):
    return mk_tva(
        name="tva2", value=700, default=0, compte_cg="TVA0002", code="CTVA0002"
    )


@pytest.fixture
def company(mk_company):
    return mk_company(
        name="company",
        email="company@c.fr",
        code_compta="COMP_CG",
        contribution=None,
    )


@pytest.fixture
def customer(mk_customer, company):
    return mk_customer(
        compte_tiers="CUSTOMER",
        compte_cg="CG_CUSTOMER",
        company=company,
        company_id=company.id,
    )


@pytest.fixture
def supplier(mk_supplier, company):
    return mk_supplier(
        compte_tiers="SUPPLIER",
        compte_cg="CG_SUPPLIER",
        company=company,
        company_id=company.id,
    )


@pytest.fixture
def bank(mk_bankaccount):
    return mk_bankaccount(
        label="banque",
        code_journal="CODE_JOURNAL_BANK",
        compte_cg="COMPTE_CG_BANK",
    )


@pytest.fixture
def expense_type(mk_expense_type):
    return mk_expense_type(
        code="ETYPE1",
        code_tva="CODETVA",
        compte_tva="COMPTETVA",
        contribution=True,
    )


@pytest.fixture
def contribution_module(mk_custom_invoice_book_entry_module):
    return mk_custom_invoice_book_entry_module(
        name="contribution",
        title="{company.name}",
        percentage=10.0,
        compte_cg_credit="CG_CONTRIB_CREDIT",
        compte_cg_debit="CG_CONTRIB_DEBIT",
        doctype="invoice",
    )


@pytest.fixture
def internalcontribution_module(mk_custom_invoice_book_entry_module):
    return mk_custom_invoice_book_entry_module(
        name="contribution",
        title="{company.name}",
        percentage=5.0,
        compte_cg_credit="INTERNAL_CG_CONTRIB_CREDIT",
        compte_cg_debit="INTERNAL_CG_CONTRIB_DEBIT",
        doctype="internalinvoice",
    )


@pytest.fixture
def insurance_module(mk_custom_invoice_book_entry_module):
    return mk_custom_invoice_book_entry_module(
        name="insurance",
        title="{company.name}",
        percentage=5.0,
        compte_cg_credit="CG_ASSUR1",
        compte_cg_debit="CG_ASSUR2",
        doctype="invoice",
    )


@pytest.fixture
def internalinsurance_module(mk_custom_invoice_book_entry_module):
    return mk_custom_invoice_book_entry_module(
        name="insurance",
        title="{company.name}",
        percentage=5.0,
        compte_cg_credit="INTERNAL_CG_ASSUR1",
        compte_cg_debit="INTERNAL_CG_ASSUR2",
        doctype="internalinvoice",
    )
