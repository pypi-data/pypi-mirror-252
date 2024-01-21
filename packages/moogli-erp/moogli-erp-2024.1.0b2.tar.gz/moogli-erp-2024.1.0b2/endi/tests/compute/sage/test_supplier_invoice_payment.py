import datetime
import pytest

from endi.compute.sage.supplier_invoice_payment import (
    SageSupplierPaymentMain,
    InternalSageSupplierPaymentMain,
    SageSupplierUserPaymentMain,
    SageSupplierUserPaymentWaiver,
)


@pytest.fixture
def supplier_invoice(mk_supplier_invoice, company, supplier):
    result = mk_supplier_invoice(
        company=company,
        supplier=supplier,
    )
    result.official_number = "SINV_01"
    return result


@pytest.fixture
def supplier_payment(mk_supplier_payment, supplier_invoice):
    res = mk_supplier_payment(
        supplier_invoice=supplier_invoice,
        bank_remittance_id="test",
        date=datetime.datetime(2021, 3, 18),
        mode="virt",
    )
    return res


@pytest.fixture
def supplier_invoice_hybrid(mk_supplier_invoice, user):
    return mk_supplier_invoice(cae_percentage=80, payer=user, official_number="OFN1234")


@pytest.fixture
def user_payment(mk_user_payment, supplier_invoice_hybrid):
    return mk_user_payment(
        supplier_invoice=supplier_invoice_hybrid,
        bank_remittance_id="test",
        date=datetime.datetime(2021, 3, 18),
        mode="virt",
    )


@pytest.fixture
def sage_user_payment_main(user_payment, config_request):
    result = SageSupplierUserPaymentMain(None, config_request)
    result.set_payment(user_payment)
    return result


@pytest.fixture
def sage_user_payment_waiver(config_request, user_payment):
    result = SageSupplierUserPaymentWaiver(None, config_request)
    result.set_payment(user_payment)
    return result


@pytest.fixture
def sage_supplier_payment_main(supplier_payment, config_request):
    result = SageSupplierPaymentMain(None, config_request)
    result.set_payment(supplier_payment)
    return result


@pytest.fixture
def internalsupplier_invoice(mk_internalsupplier_invoice, company, supplier):
    result = mk_internalsupplier_invoice(
        company=company,
        supplier=supplier,
    )
    result.official_number = "ISINV_01"
    return result


@pytest.fixture
def internalsupplier_payment(mk_internalsupplier_payment, internalsupplier_invoice):
    res = mk_internalsupplier_payment(
        supplier_invoice=internalsupplier_invoice,
        date=datetime.datetime(2021, 3, 18),
    )
    return res


@pytest.fixture
def internalsage_supplier_payment_main(internalsupplier_payment, config_request):
    result = InternalSageSupplierPaymentMain(None, config_request)
    result.set_payment(internalsupplier_payment)
    return result


class TestSageSupplierPaymentMain:
    def test_code_journal(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.code_journal == "CODE_JOURNAL_BANK"

    def test_libelle(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.libelle == "company / Rgt supplier"

    def test_date(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.date == datetime.date(2021, 3, 18)

    def test_mode(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.mode == "virt"

    def test_num_analytique(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.num_analytique == "COMP_CG"

    def test_code_taxe(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.code_taxe == "TVANDF"

    def test_reference(self, sage_supplier_payment_main):
        assert sage_supplier_payment_main.reference == "SINV_01/test"

    def test_credit_bank(self, sage_supplier_payment_main):
        a, result = sage_supplier_payment_main.credit_bank(100000000)
        assert result["credit"] == 100000000
        assert result["compte_cg"] == "COMPTE_CG_BANK"

    def test_debit_supplier(self, sage_supplier_payment_main):
        a, result = sage_supplier_payment_main.debit_supplier(100000000)
        assert result["debit"] == 100000000
        assert result["compte_cg"] == "CG_SUPPLIER"
        assert result["compte_tiers"] == "SUPPLIER"


class TestSageSupplierInvoiceuserPaymentMain:
    def test_code_journal(self, sage_user_payment_main):
        assert sage_user_payment_main.code_journal == "CODE_JOURNAL_BANK"

    def test_libelle(self, sage_user_payment_main):
        assert sage_user_payment_main.libelle == "LASTNAME / REMB FACT OFN1234"

    def test_date(self, sage_user_payment_main):
        assert sage_user_payment_main.date == datetime.date(2021, 3, 18)

    def test_mode(self, sage_user_payment_main):
        assert sage_user_payment_main.mode == "virt"

    def test_num_analytique(self, sage_user_payment_main):
        assert sage_user_payment_main.num_analytique == "COMP_CG"

    def test_code_taxe(self, sage_user_payment_main):
        assert sage_user_payment_main.code_taxe == "TVANDF"

    def test_reference(self, sage_user_payment_main):
        assert sage_user_payment_main.reference == "OFN1234/test"

    def test_credit_bank(self, sage_user_payment_main):
        a, result = sage_user_payment_main.credit_bank(100000000)
        assert result["credit"] == 100000000
        assert result["compte_cg"] == "COMPTE_CG_BANK"

    def test_debit_user(self, sage_user_payment_main, user):
        user.compte_tiers = "COMP_TIERS_USER"
        a, result = sage_user_payment_main.debit_user(100000000)
        assert result["debit"] == 100000000
        assert result["compte_cg"] == "CGNDF"
        assert result["compte_tiers"] == "COMP_TIERS_USER"


class TestSageSupplierInvoiceuserPaymentWaiver:
    def test_code_journal(self, sage_user_payment_waiver):
        assert sage_user_payment_waiver.code_journal == "JOURNAL_ABANDON"

    def test_libelle(self, sage_user_payment_waiver):
        assert sage_user_payment_waiver.libelle == "Abandon de créance LASTNAME OFN1234"

    def test_code_taxe(self, sage_user_payment_waiver):
        assert sage_user_payment_waiver.code_taxe == ""

    def test_mode(self, sage_user_payment_waiver):
        assert sage_user_payment_waiver.mode == "Abandon de créance"

    def test_credit_bank(self, sage_user_payment_waiver):
        _, entry = sage_user_payment_waiver.credit_bank(1000000)
        assert entry["compte_cg"] == "COMPTE_CG_WAIVER"
        assert entry.get("compte_tiers", "") == ""
        assert entry["credit"] == 1000000


class TestInternalSageSupplierPaymentMain:
    def test_code_journal(self, internalsage_supplier_payment_main):
        assert (
            internalsage_supplier_payment_main.code_journal == "INTERNAL_FRNS_JOURNAL"
        )

    def test_libelle(self, internalsage_supplier_payment_main):
        assert (
            internalsage_supplier_payment_main.libelle
            == "company / Rgt Interne supplier"
        )

    def test_date(self, internalsage_supplier_payment_main):
        assert internalsage_supplier_payment_main.date == datetime.date(2021, 3, 18)

    def test_mode(self, internalsage_supplier_payment_main):
        assert internalsage_supplier_payment_main.mode == "interne"

    def test_num_analytique(self, internalsage_supplier_payment_main):
        assert internalsage_supplier_payment_main.num_analytique == "COMP_CG"

    def test_code_taxe(self, internalsage_supplier_payment_main):
        assert internalsage_supplier_payment_main.code_taxe == "TVANDF"

    def test_reference(self, internalsage_supplier_payment_main):
        assert internalsage_supplier_payment_main.reference == "ISINV_01"

    def test_credit_bank(self, internalsage_supplier_payment_main):
        a, result = internalsage_supplier_payment_main.credit_bank(100000000)
        assert result["credit"] == 100000000
        assert result["compte_cg"] == "INTERNAL_BANK_CG_ENCAISSEMENT"

    def test_debit_supplier(self, internalsage_supplier_payment_main):
        a, result = internalsage_supplier_payment_main.debit_supplier(100000000)
        assert result["debit"] == 100000000
        assert result["compte_cg"] == "CG_SUPPLIER"
        assert result["compte_tiers"] == "SUPPLIER"
