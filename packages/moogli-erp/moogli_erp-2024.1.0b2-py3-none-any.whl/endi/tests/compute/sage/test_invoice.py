from endi.utils.compat import Iterable
import datetime
from typing import Set

import pytest

from endi.compute.sage.invoice import (
    SageFacturation,
    InternalSageFacturation,
    SageRGInterne,
    SageRGClient,
    CustomBookEntryFactory,
    InternalCustomBookEntryFactory,
    InvoiceExportProducer,
    InvoiceExportGroupper,
    InternalInvoiceExportProducer,
)
from endi.compute.sage.invoice import (
    SageInvoice,
)
from endi.models.task import TaskLine, TaskLineGroup, DiscountLine
from endi.tests.tools import Dummy
from .base import BaseBookEntryTest


@pytest.fixture
def invoice(
    mk_invoice,
    dbsession,
    def_dummy_tva,
    dummy_tva_computer,
    mk_product,
    customer,
    company,
    contribution_module,
    internalcontribution_module,
    insurance_module,
    internalinsurance_module,
):
    p1 = mk_product(name="product 1", compte_cg="P0001", tva=def_dummy_tva)
    p2 = mk_product(name="product 2", compte_cg="P0002", tva=dummy_tva_computer)
    invoice = mk_invoice(mode="ht")
    lines = []
    line1 = TaskLine(
        cost=10000000,
        quantity=1,
        tva=def_dummy_tva.value,
        product=p1,
    )
    lines.append(line1)
    line2 = TaskLine(
        cost=10000000,
        quantity=1,
        tva=def_dummy_tva.value,
        product=p1,
    )
    lines.append(line2)
    line3 = TaskLine(
        cost=10000000,
        quantity=1,
        tva=dummy_tva_computer.value,
        product=p2,
    )
    lines.append(line3)
    invoice.company = company
    invoice.customer = customer
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    invoice.default_tva = def_dummy_tva.value
    invoice.expenses_tva = def_dummy_tva.value
    invoice.date = datetime.date(2013, 2, 2)
    invoice.official_number = "INV_001"
    invoice.expenses_ht = 10000000
    invoice.expenses = 10000000
    return invoice


@pytest.fixture
def invoice_bug2934(tva10, tva20, empty_task, customer, company, mk_product):
    p1 = mk_product(tva=tva10, name="p1", compte_cg="P0001")
    # same compte, different tva:
    p2 = mk_product(tva=tva20, name="p2", compte_cg="P0001")
    # same tva, different compte:
    p3 = mk_product(tva=tva10, name="p3", compte_cg="P0003")
    # same tva, same compte
    p4 = mk_product(tva=tva10, name="p4", compte_cg="P0001")

    lines = [
        TaskLine(cost=100000000, tva=p1.tva.value, product=p1),
        TaskLine(cost=200000000, tva=p2.tva.value, product=p2),
        TaskLine(cost=500000000, tva=p3.tva.value, product=p3),
        TaskLine(cost=900000000, tva=p4.tva.value, product=p4),
    ]
    invoice = empty_task
    invoice.default_tva = tva20.value
    invoice.expenses_tva = tva20.value
    invoice.date = datetime.date(2016, 5, 4)
    invoice.company = company
    invoice.official_number = "INV_002"
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    return invoice


@pytest.fixture
def invoice_bug363(
    def_dummy_tva,
    dummy_tva10,
    company,
    customer,
    mk_product,
    mk_invoice,
):
    prod = mk_product(name="product 2", compte_cg="P0002", tva=dummy_tva10)
    lines = []
    invoice = mk_invoice(mode="ht")

    for cost, qtity in (
        (15000000, 1),
        (2000000, 86),
        (-173010000, 1),
        (10000000, 1),
        (-201845000, 1),
        (4500000, 33),
        (1800000, 74),
        (3500000, 28),
    ):
        lines.append(
            TaskLine(
                cost=cost,
                quantity=qtity,
                tva=dummy_tva10.value,
                product=prod,
            )
        )

    invoice.company = company
    invoice.customer = customer
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    invoice.default_tva = def_dummy_tva.value
    invoice.expenses_tva = def_dummy_tva.value
    invoice.date = datetime.date(2013, 2, 2)
    invoice.official_number = "INV_001"
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


@pytest.fixture
def invoice_bug400(def_dummy_tva, dummy_tva20, mk_product, mk_invoice):
    prod = mk_product(name="product 2", compte_cg="P0002", tva=dummy_tva20)
    lines = []

    for cost, qtity in ((22112500, 1),):
        lines.append(
            TaskLine(
                cost=cost,
                quantity=qtity,
                tva=dummy_tva20.value,
                product=prod,
            )
        )

    invoice = mk_invoice(mode="ht")
    invoice.default_tva = def_dummy_tva.value
    invoice.expenses_tva = def_dummy_tva.value
    invoice.date = datetime.date(2013, 2, 2)
    invoice.official_number = "INV_001"
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


@pytest.fixture
def invoice_issue1160(tva, mk_product, mk_invoice, customer, company):
    """
    Credit et debit négatif
    """
    prod = mk_product(name="product 2", compte_cg="P0002", tva=tva)
    lines = []

    for cost, qtity in ((-22112500, 1),):
        lines.append(
            TaskLine(
                cost=cost,
                quantity=qtity,
                tva=tva.value,
                product=prod,
            )
        )

    invoice = mk_invoice(mode="ht")
    invoice.company = company
    invoice.customer = customer
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    invoice.date = datetime.date(2019, 3, 29)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_001"
    invoice.expenses_ht = 0
    return invoice


@pytest.fixture
def invoice_discount(def_dummy_tva, dummy_tva_computer, invoice):
    discount1 = DiscountLine(
        amount=10000000,
        tva=def_dummy_tva.value,
    )
    discount2 = DiscountLine(
        amount=10000000,
        tva=dummy_tva_computer.value,
    )
    invoice.discounts = [discount1, discount2]
    return invoice


@pytest.fixture
def internalinvoice(
    dbsession,
    mk_internalinvoice,
    mk_product,
    mk_tva,
    mk_task_line,
    mk_discount_line,
    customer,
    company,
    contribution_module,
    internalcontribution_module,
    insurance_module,
    internalinsurance_module,
):
    tva = mk_tva(name="test", value=0, compte_cg="TVAINT")
    product = mk_product(
        tva=tva,
        name="interne",
        internal=True,
        compte_cg="70400000",
    )
    line = mk_task_line(
        description="presta",
        cost=100000000,
        quantity=1,
        tva=tva.value,
        product=product,
    )
    customer.compte_cg = "41100000"
    dbsession.merge(customer)
    dbsession.flush()
    invoice = mk_internalinvoice(customer=customer, company=company)
    invoice.official_number = "INV_I01"
    invoice.date = datetime.date(2013, 2, 2)
    invoice.line_groups = [TaskLineGroup(lines=[line])]
    invoice.discounts.append(mk_discount_line(amount=5000000, tva=0))
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def sageinvoice(def_dummy_tva, invoice, app_config):
    return SageInvoice(
        invoice=invoice,
        config=app_config,
        default_tva=def_dummy_tva,
    )


@pytest.fixture
def internalsageinvoice(def_dummy_tva, internalinvoice, app_config):
    wrapped_invoice = SageInvoice(
        invoice=internalinvoice,
        config=app_config,
        default_tva=def_dummy_tva,
    )
    return wrapped_invoice


@pytest.fixture
def sageinvoice_discount(def_dummy_tva, invoice_discount, app_config):
    return SageInvoice(
        invoice=invoice_discount, config=app_config, default_tva=def_dummy_tva
    )


@pytest.fixture
def sageinvoice_bug2934(def_dummy_tva, invoice_bug2934, app_config):
    return SageInvoice(
        invoice=invoice_bug2934,
        config=app_config,
        default_tva=def_dummy_tva,
    )


@pytest.fixture
def sageinvoice_bug363(def_dummy_tva, invoice_bug363, app_config):
    return SageInvoice(
        invoice=invoice_bug363,
        config=app_config,
        default_tva=def_dummy_tva,
    )


@pytest.fixture
def sageinvoice_bug400(def_dummy_tva, invoice_bug400, app_config):
    return SageInvoice(
        invoice=invoice_bug400,
        config=app_config,
        default_tva=def_dummy_tva,
    )


@pytest.fixture
def internalcustom_module(mk_custom_invoice_book_entry_module):
    return mk_custom_invoice_book_entry_module(
        doctype="internalinvoice",
    )


def test_get_product(sageinvoice):
    sageinvoice.products["cg_p1", "cg_tva1"] = {"test_key": "test"}
    assert "test_key" in sageinvoice.get_product(
        ("cg_p1", "cg_tva1"), "cg_p1", "cg_tva1", "dontcare", 20
    )
    assert (
        len(
            list(
                sageinvoice.get_product(
                    ("2", "tva_compte_cg"), "2", "tva_compte_cg", "tva_code", 20
                ).keys()
            )
        )
        == 4
    )


def test_populate_invoice_lines(sageinvoice):
    sageinvoice._populate_invoice_lines()
    sageinvoice._round_products()
    assert set(sageinvoice.products.keys()) == set(
        [("P0001", "TVA0001"), ("P0002", "TVA0002")]
    )
    assert sageinvoice.products[("P0001", "TVA0001")]["ht"] == 20000000
    assert sageinvoice.products[("P0001", "TVA0001")]["tva"] == 3920000
    assert sageinvoice.products[("P0002", "TVA0002")]["ht"] == 10000000
    assert sageinvoice.products[("P0002", "TVA0002")]["tva"] == 700000


def test_populate_discount_lines(sageinvoice_discount):
    sageinvoice_discount._populate_discounts()
    sageinvoice_discount._round_products()
    expected_key = "rrr"
    assert list(sageinvoice_discount.products.keys()) == [expected_key]
    assert sageinvoice_discount.products[expected_key]["code_tva"] == "CODE_TVA_RRR"
    assert sageinvoice_discount.products[expected_key]["compte_cg_tva"] == "CG_TVA_RRR"
    assert sageinvoice_discount.products[expected_key]["ht"] == 20000000
    assert sageinvoice_discount.products[expected_key]["tva"] == 2660000


def test_populate_discount_lines_without_compte_rrr(sageinvoice_discount):
    from endi.compute.sage import MissingData

    # If one compte_cg_tva_rrr is not def
    # No entry should be returned
    sageinvoice_discount.config.pop("compte_rrr")
    with pytest.raises(MissingData):
        sageinvoice_discount._populate_discounts()


def test_populate_discount_lines_without_compte_cg_tva(sageinvoice_discount):
    from endi.compute.sage import MissingData

    # If one compte_cg_tva_rrr is not def
    # No entry should be returned
    sageinvoice_discount.config.pop("compte_cg_tva_rrr")
    with pytest.raises(MissingData):
        sageinvoice_discount._populate_discounts()


def test_populate_discount_lines_without_code_tva(sageinvoice_discount):
    # If the code tva is not def, it should work
    sageinvoice_discount.config.pop("code_tva_rrr")
    sageinvoice_discount._populate_discounts()
    assert list(sageinvoice_discount.products.keys()) != []


def test_round_products(sageinvoice_bug400):
    sageinvoice_bug400._populate_invoice_lines()
    sageinvoice_bug400._round_products()
    assert list(sageinvoice_bug400.products.values())[0]["ht"] == 22113000


def test_populate_expenses(sageinvoice):
    sageinvoice.expense_tva_compte_cg = "TVA0001"
    sageinvoice._populate_expenses()
    sageinvoice._round_products()
    expected_key = ("CG_FA", "TVA0001")
    assert list(sageinvoice.products.keys()) == [expected_key]
    assert sageinvoice.products[expected_key]["ht"] == 20000000
    assert sageinvoice.products[expected_key]["tva"] == 1960000


class TestSageFacturation(BaseBookEntryTest):
    factory = SageFacturation

    def test__has_tva_value(self):
        product = {"tva": 0.5}
        assert SageFacturation._has_tva_value(product)
        product = {"tva": 0.0}
        assert not SageFacturation._has_tva_value(product)
        product = {"tva": -0.5}
        assert SageFacturation._has_tva_value(product)

    def test_credit_totalht(self, sageinvoice, config_request):
        res = {
            "libelle": "customer company",
            "compte_cg": "P0001",
            "num_analytique": "COMP_CG",
            "code_tva": "CTVA0001",
            "credit": 20000000,
        }
        method = "credit_totalht"
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_credit_tva(self, sageinvoice, config_request):
        res = {
            "libelle": "customer company",
            "compte_cg": "TVA0001",
            "num_analytique": "COMP_CG",
            "code_tva": "CTVA0001",
            "credit": 3920000,
        }
        method = "credit_tva"
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_debit_ttc(self, config_request, sageinvoice):
        method = "debit_ttc"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_CUSTOMER",
            "num_analytique": "COMP_CG",
            "compte_tiers": "CUSTOMER",
            "debit": 23920000,
            "echeance": datetime.date(2013, 3, 4),
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_discount_ht(self, sageinvoice_discount, config_request):
        # REF #307 : https://framagit.org/endi/endi/issues/307
        method = "credit_totalht"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_RRR",
            "num_analytique": "COMP_CG",
            "code_tva": "CODE_TVA_RRR",
            "debit": 20000000,
        }
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            "CG_RRR",
            "CG_TVA_RRR",
            "rrr",
        )

    def test_discount_tva(self, sageinvoice_discount, config_request):
        # REF #307 : https://framagit.org/endi/endi/issues/307
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_TVA_RRR",
            "num_analytique": "COMP_CG",
            "code_tva": "CODE_TVA_RRR",
            "debit": 1960000 + 700000,
        }
        method = "credit_tva"
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            "CG_RRR",
            "CG_TVA_RRR",
            "rrr",
        )

    def test_discount_ttc(self, config_request, sageinvoice_discount):
        # REF #307 : https://framagit.org/endi/endi/issues/307
        method = "debit_ttc"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_CUSTOMER",
            "num_analytique": "COMP_CG",
            "compte_tiers": "CUSTOMER",
            "credit": 20000000 + 1960000 + 700000,
            "echeance": datetime.date(2013, 3, 4),
        }
        self._test_product_book_entry(
            config_request,
            sageinvoice_discount,
            method,
            res,
            "CG_RRR",
            "CG_TVA_RRR",
            "rrr",
        )

    def test_bug363(self, config_request, sageinvoice_bug363):
        res = {
            "libelle": "customer company",
            "compte_cg": "TVA10",
            "num_analytique": "COMP_CG",
            "code_tva": "CTVA10",
            "credit": 20185000,
        }
        method = "credit_tva"
        self._test_product_book_entry(
            config_request,
            sageinvoice_bug363,
            method,
            res,
            "P0002",
            "TVA10",
        )

    def test_group_by_tva_and_compte_cg(self, sageinvoice_bug2934):
        # Ref #2934
        sageinvoice_bug2934.populate()
        assert len(sageinvoice_bug2934.products) == 3
        l1, l2, l3 = sageinvoice_bug2934.products.values()
        # L1 is group of line 1 and line 4 because same tva AND same compte_cg
        assert l1 == {
            "compte_cg_produit": "P0001",
            "compte_cg_tva": "TVA10",
            "code_tva": "CTVA10",
            "tva": 90000000 + 10000000,
            "ht": 900000000 + 100000000,
        }
        assert l2 == {
            "compte_cg_produit": "P0001",
            "compte_cg_tva": "TVA20",
            "code_tva": "CTVA20",
            "tva": 40000000,
            "ht": 200000000,
        }
        assert l3 == {
            "compte_cg_produit": "P0003",
            "compte_cg_tva": "TVA10",
            "code_tva": "CTVA10",
            "tva": 50000000,
            "ht": 500000000,
        }


class TestSageContribution(BaseBookEntryTest):
    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="CG_CONTRIB_DEBIT",
                compte_cg_credit="CG_CONTRIB_CREDIT",
                percentage=10.0,
                enabled=True,
                label_template="{client.name} {entreprise.name}",
                name="contribution",
            ),
        )

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_CONTRIB_DEBIT",
            "num_analytique": "COMP_CG",
            "debit": 4000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": "customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "COMP_CG",
            "credit": 4000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "debit": 4000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_CONTRIB_CREDIT",
            "num_analytique": "NUM_ANA",
            "credit": 4000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestCustomAssurance(BaseBookEntryTest):
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    # Migrate the export module Assurance to a custom module
    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="CG_ASSUR",
                compte_cg_credit="CG_ASSUR",
                percentage=5,
                label_template="{client.label} {entreprise.name}",
                name="insurance",
            ),
        )

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_ASSUR",
            "num_analytique": "COMP_CG",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": "customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "COMP_CG",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_ASSUR",
            "num_analytique": "NUM_ANA",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestCustomCGScop(BaseBookEntryTest):
    # Migrate the export module CGScop to a custom module
    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="CG_SCOP",
                compte_cg_credit="CG_DEB",
                percentage=5,
                label_template="{client.label} {entreprise.name}",
                name="",
            ),
        )

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_SCOP",
            "num_analytique": "COMP_CG",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": "customer company",
            "num_analytique": "COMP_CG",
            "compte_cg": "BANK_CG",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {
            "libelle": "customer company",
            "compte_cg": "CG_DEB",
            "num_analytique": "NUM_ANA",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestCustomBookEntryFactory(BaseBookEntryTest):
    # Replaced SageContributionOrganic
    libelle = "Contribution Organic customer company"

    def build_factory(self, config_request):
        return CustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="CG_ORGA",
                compte_cg_credit="CG_DEB_ORGA",
                percentage=5,
                label_template="Contribution Organic {client.label} {entreprise.name}",
                name="",
            ),
        )

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": self.libelle,
            "compte_cg": "CG_ORGA",
            "num_analytique": "COMP_CG",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": self.libelle,
            "num_analytique": "COMP_CG",
            "compte_cg": "BANK_CG",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {
            "libelle": self.libelle,
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "debit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {
            "libelle": self.libelle,
            "compte_cg": "CG_DEB_ORGA",
            "num_analytique": "NUM_ANA",
            "credit": 2000000,
        }
        self._test_invoice_book_entry(config_request, sageinvoice, method, res)


class TestSageRGInterne(BaseBookEntryTest):
    factory = SageRGInterne

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": "RG COOP customer company",
            "compte_cg": "CG_RG_INT",
            "num_analytique": "COMP_CG",
            "debit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": "RG COOP customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "COMP_CG",
            "credit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_debit_cae(self, config_request, sageinvoice):
        method = "debit_cae"
        res = {
            "libelle": "RG COOP customer company",
            "compte_cg": "BANK_CG",
            "num_analytique": "NUM_ANA",
            "debit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_credit_cae(self, config_request, sageinvoice):
        method = "credit_cae"
        res = {
            "libelle": "RG COOP customer company",
            "compte_cg": "CG_RG_INT",
            "num_analytique": "NUM_ANA",
            "credit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)


class TestSageRGClient(BaseBookEntryTest):
    factory = SageRGClient

    def test_debit_company(self, config_request, sageinvoice):
        method = "debit_company"
        res = {
            "libelle": "RG customer company",
            "compte_cg": "CG_RG_EXT",
            "num_analytique": "COMP_CG",
            "echeance": datetime.date(2014, 2, 2),
            "debit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)

    def test_credit_company(self, config_request, sageinvoice):
        method = "credit_company"
        res = {
            "libelle": "RG customer company",
            "num_analytique": "COMP_CG",
            "compte_cg": "CG_CUSTOMER",
            "compte_tiers": "CUSTOMER",
            "echeance": datetime.date(2014, 2, 2),
            "credit": 1196000,
        }
        self._test_product_book_entry(config_request, sageinvoice, method, res)


class TestInvoiceExportProducer:
    def get_one(self, request):
        return InvoiceExportProducer(None, request)

    def test_modules(self, config_request, app_config):
        config_request.config = app_config
        exporter = self.get_one(config_request)
        assert len(exporter.modules) == 2
        sage_factories = [SageFacturation, SageRGInterne]
        for fact in sage_factories:
            assert True in [isinstance(module, fact) for module in exporter.modules]

    def test_get_item_book_entries(
        self, config_request, app_config, invoice_issue1160, tva
    ):
        config_request.config = app_config
        exporter = self.get_one(config_request)
        for entry in exporter._get_item_book_entries(invoice_issue1160):
            assert entry.get("credit", 0) >= 0
            assert entry.get("debit", 0) >= 0


class TestInternalSageFacturation(BaseBookEntryTest):
    code_journal = "INTERNAL_JOURNAL"
    factory = InternalSageFacturation

    def test__get_config_value(self, config_request):
        factory = self.build_factory(config_request)
        assert factory._get_config_value("compte_rrr") == "INTERNAL_CG_RRR"

    def test__has_tva_value(self, config_request):
        factory = self.build_factory(config_request)
        assert not factory._has_tva_value("15")

    def test_credit_totalht(self, internalsageinvoice, config_request):
        res = {
            "libelle": "customer company",
            "compte_cg": "70400000",
            "num_analytique": "COMP_CG",
            "code_tva": "",
            "credit": 100000000,
        }
        method = "credit_totalht"
        self._test_product_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
            prod_cg="70400000",
            tva_cg="TVAINT",
        )

    def test_debit_ttc(self, config_request, internalsageinvoice):
        method = "debit_ttc"
        res = {
            "libelle": "customer company",
            "compte_cg": "41100000",
            "num_analytique": "COMP_CG",
            "compte_tiers": "CUSTOMER",
            "debit": 100000000,
            "echeance": datetime.date(2013, 3, 4),
        }
        self._test_product_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
            prod_cg="70400000",
            tva_cg="TVAINT",
        )

    def test_discount_ht(self, internalsageinvoice, config_request):
        # REF #307 : https://framagit.org/endi/endi/issues/307
        method = "credit_totalht"
        res = {
            "libelle": "customer company",
            "compte_cg": "INTERNAL_CG_RRR",
            "num_analytique": "COMP_CG",
            "code_tva": "",
            "debit": 5000000,
        }
        self._test_product_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
            "INTERNAL_CG_RRR",
            "TVAINT",
            "rrr",
        )

    def test_discount_ttc(self, config_request, internalsageinvoice):
        # REF #307 : https://framagit.org/endi/endi/issues/307
        method = "debit_ttc"
        res = {
            "libelle": "customer company",
            "compte_cg": "41100000",
            "num_analytique": "COMP_CG",
            "compte_tiers": "CUSTOMER",
            "credit": 5000000,
            "echeance": datetime.date(2013, 3, 4),
        }
        self._test_product_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
            "INTERNAL_CG_RRR",
            "TVAINT",
            "rrr",
        )


class TestInternalSageContribution(BaseBookEntryTest):
    code_journal = "INTERNAL_JOURNAL"

    def build_factory(
        self,
        config_request,
    ):
        return InternalCustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="INTERNAL_CG_CONTRIB_DEBIT",
                compte_cg_credit="INTERNAL_CG_CONTRIB_CREDIT",
                percentage=5.0,
                enabled=True,
                label_template="contrib {client.name} {entreprise.name}",
                name="contribution",
            ),
        )

    def test__get_config_value(self, config_request, internalinvoice):
        factory = self.build_factory(config_request)
        assert factory._get_config_value("compte_rrr") == "INTERNAL_CG_RRR"

    def test_get_contribution(self, config_request, company, internalinvoice):
        factory = self.build_factory(config_request)
        company.contribution = 10
        factory.company = company
        assert factory.get_contribution() == 5
        company.internalcontribution = 6
        assert factory.get_contribution() == 6

    def test_debit_company(self, config_request, company, internalsageinvoice):
        method = "debit_company"
        res = {
            "libelle": "contrib customer company",
            "compte_cg": "INTERNAL_CG_CONTRIB_DEBIT",
            "num_analytique": "COMP_CG",
            "debit": 4750000,
        }
        self._test_invoice_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
        )

    def test_credit_company(self, config_request, internalsageinvoice):
        method = "credit_company"
        res = {
            "libelle": "contrib customer company",
            "compte_cg": "INTERNAL_BANK_CG",
            "num_analytique": "COMP_CG",
            "credit": 4750000,
        }
        self._test_invoice_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
        )

    def test_debit_cae(self, config_request, internalsageinvoice):
        method = "debit_cae"
        res = {
            "libelle": "contrib customer company",
            "compte_cg": "INTERNAL_BANK_CG",
            "num_analytique": "INTERNAL_NUM_ANA",
            "debit": 4750000,
        }
        self._test_invoice_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
        )

    def test_credit_cae(self, config_request, internalsageinvoice):
        method = "credit_cae"
        res = {
            "libelle": "contrib customer company",
            "compte_cg": "INTERNAL_CG_CONTRIB_CREDIT",
            "num_analytique": "INTERNAL_NUM_ANA",
            "credit": 4750000,
        }
        self._test_invoice_book_entry(
            config_request,
            internalsageinvoice,
            method,
            res,
        )


class TestInternalCustomBookEntry:
    # Amount = 2000 0.05 * somme des ht des lignes + expense_ht
    # Migrate the export module Assurance to a custom module
    def build_factory(self, config_request):
        return InternalCustomBookEntryFactory(
            None,
            config_request,
            Dummy(
                compte_cg_debit="CG_ASSUR",
                compte_cg_credit="CG_ASSUR",
                percentage=5,
                label_template="{client.label} {entreprise.name}",
                name="",
            ),
        )

    def test_code_journal(self, config_request):
        factory = self.build_factory(config_request)
        assert factory.code_journal == "INTERNAL_JOURNAL"


class TestInternalExport:
    def test_base(self, config_request):
        exporter = InternalInvoiceExportProducer(None, config_request)
        assert len(exporter.modules) == 1

    def test_issue2762(self, config_request_with_db, internalcustom_module):
        exporter = InternalInvoiceExportProducer(None, config_request_with_db)
        assert len(exporter.modules) == 2


@pytest.fixture
def invoice_item_header():
    return [
        "code_journal",
        "date",
        "num_endi",
        "libelle",
        "type_",
        "compte_cg",
        "num_analytique",
        "code_tva",
        "debit",
        "credit",
        "_mark_customer_debit",
    ]


@pytest.fixture
def invoice_items_multi_product_account(invoice_item_header):
    """
    Output of SageInvoice
    for an invoice with two different product lines
    (compte_cg=7061… and compte_cg=7062…)
    """
    items_vals = [
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "70620000",
            None,
            "20",
            None,
            833000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "70620000",
            "ANA-0624",
            "20",
            None,
            833000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "44571200",
            None,
            "20",
            None,
            167000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "44571200",
            "ANA-0624",
            "20",
            None,
            167000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            1000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            1000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "70610000",
            None,
            "10",
            None,
            1818000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "70610000",
            "ANA-0624",
            "10",
            None,
            1818000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "44571100",
            None,
            "10",
            None,
            182000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "44571100",
            "ANA-0624",
            "10",
            None,
            182000,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            2000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            2000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "75500000",
            None,
            None,
            265200,
            None,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "75500000",
            "ANA-0624",
            None,
            265200,
            None,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "51211000",
            None,
            None,
            None,
            265200,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "51211000",
            "ANA-0624",
            None,
            None,
            265200,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "51211000",
            None,
            None,
            265200,
            None,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "51211000",
            "MDT0",
            None,
            265200,
            None,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "75500000",
            None,
            None,
            None,
            265200,
            None,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "75500000",
            "MDT0",
            None,
            None,
            26520,
            None,
        ],
    ]
    return [dict(zip(invoice_item_header, line)) for line in items_vals]


def test_invoice_export_groupper_disabled(
    invoice_items_multi_product_account,
    mk_config,
):
    items = invoice_items_multi_product_account

    # config not initialized
    groupper_disabled = InvoiceExportGroupper()
    assert groupper_disabled.group_items(items) == invoice_items_multi_product_account

    mk_config("bookentry_sales_group_customer_entries", "0")
    groupper_disabled = InvoiceExportGroupper()
    assert groupper_disabled.group_items(items) == invoice_items_multi_product_account


def to_values_set(items: Iterable[dict]) -> Set[tuple]:
    """
    basically : discards the key of dicts for easier comparison/reading

    NB: since py 3.6, dict is an ordered structure (by 1st insertion order)

    >>> to_values_set([{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    set([(1, 2), (3,4)])
    """
    return set(tuple(i.values()) for i in items)


def test_invoice_export_groupper_enabled(
    invoice_items_multi_product_account,
    mk_config,
):
    items = invoice_items_multi_product_account
    mk_config("bookentry_sales_group_customer_entries", "1")
    groupper_enabled = InvoiceExportGroupper()

    groupped_items = groupper_enabled.group_items(invoice_items_multi_product_account)
    assert len(groupped_items) == 20 - 2  # (one G and one A got groupped)
    assert to_values_set(groupped_items) - to_values_set(items) == set(
        [
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "G",
                "41100000",
                None,
                None,
                3000000,
                0,
                True,
            ),
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "A",
                "41100000",
                "ANA-0624",
                None,
                3000000,
                0,
                True,
            ),
        ]
    )


def test_invoice_export_groupper_rrr_positive_total(
    invoice_item_header,
    mk_config,
):
    # REF #3088
    items_vals = [
        # Product line
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            1000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            1000000,
            None,
            True,
        ],
        # This is RRR for 50% discount
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            None,
            400000,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            None,
            400000,
            True,
        ],
    ]
    items = [dict(zip(invoice_item_header, line)) for line in items_vals]

    mk_config("bookentry_sales_group_customer_entries", "1")
    groupper_enabled = InvoiceExportGroupper()

    groupped_items = groupper_enabled.group_items(items)
    assert to_values_set(groupped_items) == set(
        [
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "G",
                "41100000",
                None,
                None,
                600000,
                0,
                True,
            ),
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "A",
                "41100000",
                "ANA-0624",
                None,
                600000,
                0,
                True,
            ),
        ]
    )


def test_invoice_export_groupper_rrr_negative_total(
    invoice_item_header,
    mk_config,
):
    # REF #3088
    items_vals = [
        # Product line
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            1000000,
            None,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            1000000,
            None,
            True,
        ],
        # This is RRR for 50% discount
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "G",
            "41100000",
            None,
            None,
            None,
            1100000,
            True,
        ],
        [
            "VTE",
            "181021",
            "FA2021_1887",
            "Lesage SARL Adam",
            "A",
            "41100000",
            "ANA-0624",
            None,
            None,
            1100000,
            True,
        ],
    ]
    items = [dict(zip(invoice_item_header, line)) for line in items_vals]

    mk_config("bookentry_sales_group_customer_entries", "1")
    groupper_enabled = InvoiceExportGroupper()

    groupped_items = groupper_enabled.group_items(items)
    assert to_values_set(groupped_items) == set(
        [
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "G",
                "41100000",
                None,
                None,
                0,
                100000,
                True,
            ),
            (
                "VTE",
                "181021",
                "FA2021_1887",
                "Lesage SARL Adam",
                "A",
                "41100000",
                "ANA-0624",
                None,
                0,
                100000,
                True,
            ),
        ]
    )
