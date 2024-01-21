import pytest

from endi.compute.sage.supplier_invoice import (
    InternalSageSupplierInvoiceMain,
    SageSupplierInvoice,
    SageSupplierInvoiceMain,
)
from .base import BaseBookEntryTest


@pytest.fixture
def internalsupplier_invoice(
    dbsession,
    mk_internalsupplier_invoice,
    mk_supplier_invoice_line,
    mk_expense_type,
    mk_supplier,
    company,
    contribution_module,
    internalcontribution_module,
):
    supplier = mk_supplier(
        company_name="local",
        type="internal",
        compte_tiers="401INT",
        compte_cg="401INT",
    )
    type_ = mk_expense_type(
        label="Service", internal=True, contribution=True, code="60400000"
    )
    supplier_invoice = mk_internalsupplier_invoice(
        supplier=supplier,
        company=company,
    )
    line = mk_supplier_invoice_line(
        description="facture interne",
        ht=10000000,
        tva=0,
        type_id=type_.id,
        supplier_invoice=supplier_invoice,
    )
    supplier_invoice.lines = [line]
    dbsession.merge(supplier_invoice)
    dbsession.flush()
    return supplier_invoice


@pytest.fixture
def sagesupplier_invoice(
    half_cae_supplier_invoice,
    app_config,
    contribution_module,
    internalcontribution_module,
):
    result = SageSupplierInvoice(half_cae_supplier_invoice, app_config)
    result.populate()
    return result


@pytest.fixture
def internalsagesupplier_invoice(internalsupplier_invoice, app_config):
    result = SageSupplierInvoice(internalsupplier_invoice, app_config)
    result.populate()
    return result


class TestSupplierInvoiceMain(BaseBookEntryTest):
    factory = SageSupplierInvoiceMain
    code_journal = "FRNS_JOURNAL"

    def _test__credit_worker(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "CGNDF",
            "num_analytique": "COMP_CG",
            "credit": amount,
            "compte_tiers": "COMP_TIERS_USER",
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_supplier(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "CG_SUPPLIER",
            "num_analytique": "COMP_CG",
            "credit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_ht(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "ETYPE1",
            "num_analytique": "COMP_CG",
            "debit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_tva(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "COMPTETVA",
            "num_analytique": "COMP_CG",
            "debit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_company(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "CG_CONTRIB_DEBIT",
            "num_analytique": "COMP_CG",
            "credit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_company(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "BANK_CG",
            "num_analytique": "COMP_CG",
            "debit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_cae(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "credit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_cae(self, line, amount):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "CG_CONTRIB_CREDIT",
            "num_analytique": "NUM_ANA",
            "debit": amount,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def test_yield_entries(self, sagesupplier_invoice, config_request):
        factory = self.build_factory(config_request)
        factory.set_supplier_invoice(sagesupplier_invoice)
        lines = iter(factory.yield_entries())

        self._test__credit_supplier(next(lines), 550)
        self._test__credit_worker(next(lines), 549)
        self._test__debit_ht(next(lines), 1000)
        self._test__debit_tva(next(lines), 99)
        self._test__credit_company(next(lines), 100)
        self._test__debit_company(next(lines), 100)
        self._test__credit_cae(next(lines), 100)
        self._test__debit_cae(next(lines), 100)

        self._test__credit_supplier(next(lines), 2)
        self._test__credit_worker(next(lines), 2)
        self._test__debit_ht(next(lines), 3)
        self._test__debit_tva(next(lines), 1)
        self._test__credit_company(next(lines), 0)
        self._test__debit_company(next(lines), 0)
        self._test__credit_cae(next(lines), 0)
        self._test__debit_cae(next(lines), 0)


class TestSupplierInvoiceMainTvaOnMargin(BaseBookEntryTest):
    factory = SageSupplierInvoiceMain
    code_journal = "FRNS_JOURNAL"

    def _test__debit_ht(self, line):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "ETYPETVAOM",
            "num_analytique": "COMP_CG",
            "debit": 1000 + 99,  # ttc
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_tva_on_magin(self, line):
        res = {
            "libelle": "company / Fact. supplier",
            "compte_cg": "CG_TVA_OM",
            "num_analytique": "COMP_CG",
            "credit": 99,  # tva
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def test_tva_on_margin(
        self,
        dbsession,
        sagesupplier_invoice,
        expense_type_tva_on_margin,
        config_request,
    ):
        for l in sagesupplier_invoice.supplier_invoice.lines:
            l.expense_type = expense_type_tva_on_margin
            dbsession.merge(l)
        dbsession.merge(sagesupplier_invoice.supplier_invoice)
        dbsession.flush()
        sagesupplier_invoice.populate()

        factory = self.build_factory(config_request)
        factory.set_supplier_invoice(sagesupplier_invoice)
        lines = list(factory.yield_entries())

        # expense_type_tva_on_margin.contribution == False
        # So no contribution lines
        assert len(lines) == 8
        # Check only changed entries of first line
        self._test__debit_ht(lines[2])
        self._test__credit_tva_on_magin(lines[3])


class TestInternalSupplierInvoiceMain(BaseBookEntryTest):
    factory = InternalSageSupplierInvoiceMain
    code_journal = "INTERNAL_FRNS_JOURNAL"

    def _test__credit(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "401INT",
            "num_analytique": "COMP_CG",
            "credit": 10000000,
            "compte_tiers": "401INT",
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_ht(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "60400000",
            "num_analytique": "COMP_CG",
            "debit": 10000000,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_company(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "INTERNAL_CG_CONTRIB_DEBIT",
            "num_analytique": "COMP_CG",
            "credit": 500000,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_company(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "INTERNAL_BANK_CG",
            "num_analytique": "COMP_CG",
            "debit": 500000,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__credit_cae(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "INTERNAL_BANK_CG",
            "num_analytique": "INTERNAL_NUM_ANA",
            "credit": 500000,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def _test__debit_cae(self, line):
        res = {
            "libelle": "company / Fact Interne local",
            "compte_cg": "INTERNAL_CG_CONTRIB_CREDIT",
            "num_analytique": "INTERNAL_NUM_ANA",
            "debit": 500000,
        }
        gen_line, ana_line = line
        for key, value in res.items():
            assert ana_line.get(key) == value

    def test_yield_entries(self, internalsagesupplier_invoice, config_request):
        factory = self.build_factory(config_request)
        factory.set_supplier_invoice(internalsagesupplier_invoice)
        lines = list(factory.yield_entries())
        line = lines[0]
        self._test__credit(line)
        line = lines[1]
        self._test__debit_ht(line)
        line = lines[2]
        self._test__credit_company(line)
        line = lines[3]
        self._test__debit_company(line)
        line = lines[4]
        self._test__credit_cae(line)
        line = lines[5]
        self._test__debit_cae(line)

    def test_account_cascading(
        self, dbsession, internalsagesupplier_invoice, config_request
    ):
        factory = self.build_factory(config_request)
        internalsagesupplier_invoice.supplier_invoice.supplier.compte_tiers = None
        dbsession.merge(internalsagesupplier_invoice.supplier_invoice.supplier)
        dbsession.flush()
        factory.set_supplier_invoice(internalsagesupplier_invoice)
        lines = list(factory.yield_entries())
        line = lines[0][1]
        assert line["compte_tiers"] == "CAE_TIERS_INTERNE_FRN"

    def test_get_contribution(
        self,
        config_request,
        company,
        internalcontribution_module,
        contribution_module,
    ):
        factory = self.build_factory(config_request)
        company.contribution = 10
        factory.company = company
        assert factory.get_contribution() == 5
        company.internalcontribution = 6
        assert factory.get_contribution() == 6
