from endi.utils.compat import Iterable
import datetime
import pytest

from endi.compute.sage.payment import (
    SagePaymentMain,
    SagePaymentTva,
    SagePaymentRemittance,
    InternalSagePaymentMain,
    PaymentExportGroupper,
)

from endi.compute.sage.base import generate_general_entry


@pytest.fixture
def remittance(bank, mk_bank_remittance):
    return mk_bank_remittance(
        id="REM_ID",
        payment_mode="chèque",
        remittance_date=datetime.date.today(),
        closed=1,
        bank=bank,
        bank_id=bank.id,
    )


@pytest.fixture
def internalinvoice(
    dbsession,
    mk_internalinvoice,
    mk_product,
    mk_tva,
    mk_task_line,
    mk_discount_line,
    mk_task_line_group,
    customer,
    company,
):
    tva = mk_tva(name="test", value=0)
    product = mk_product(
        tva=tva,
        name="interne",
        internal=True,
        compte_cg="70400000",
    )
    line = mk_task_line(
        description="presta", cost=100000000, quantity=1, tva=tva.value, product=product
    )
    customer.compte_cg = "41100000"
    dbsession.merge(customer)
    dbsession.flush()
    invoice = mk_internalinvoice(customer=customer, company=company)
    invoice.official_number = "INV_I01"
    invoice.date = datetime.date(2013, 2, 2)
    invoice.line_groups = [mk_task_line_group(lines=[line])]
    invoice.discounts.append(mk_discount_line(amount=5000000, tva=0))
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def invoice(
    mk_invoice,
    dbsession,
    def_dummy_tva,
    dummy_tva_computer,
    mk_product,
    customer,
    company,
    mk_task_line,
    mk_task_line_group,
):
    p1 = mk_product(name="product 1", compte_cg="P0001", tva=def_dummy_tva)
    p2 = mk_product(name="product 2", compte_cg="P0002", tva=dummy_tva_computer)
    invoice = mk_invoice(mode="ht")
    lines = []
    line1 = mk_task_line(
        cost=10000000,
        tva=def_dummy_tva.value,
        product=p1,
    )
    lines.append(line1)
    line2 = mk_task_line(
        cost=10000000,
        tva=def_dummy_tva.value,
        product=p1,
    )
    lines.append(line2)
    line3 = mk_task_line(
        cost=10000000,
        tva=dummy_tva_computer.value,
        product=p2,
    )
    lines.append(line3)
    invoice.company = company
    invoice.customer = customer
    invoice.line_groups = [mk_task_line_group(lines=lines)]
    invoice.default_tva = def_dummy_tva.value
    invoice.expenses_tva = def_dummy_tva.value
    invoice.date = datetime.date(2013, 2, 2)
    invoice.official_number = "INV_001"
    invoice.expenses_ht = 10000000
    invoice.expenses = 10000000
    return invoice


@pytest.fixture
def payment(mk_payment, def_dummy_tva, remittance):
    return mk_payment(
        amount=10000000,
        mode="chèque",
        tva=def_dummy_tva,
        bank_remittance=remittance,
    )


@pytest.fixture
def internalpayment(internalinvoice):
    from endi.models.task.internalpayment import InternalPayment

    p = InternalPayment(
        amount=10000000,
        date=datetime.datetime.now(),
    )
    internalinvoice.payments = [p]
    return internalinvoice.payments[0]


@pytest.fixture
def sagepayment(payment, config_request):
    factory = SagePaymentMain(None, config_request)
    factory.set_payment(payment)
    return factory


@pytest.fixture
def internalsagepayment_module(internalpayment, config_request):
    factory = InternalSagePaymentMain(None, config_request)
    factory.set_payment(internalpayment)
    return factory


@pytest.fixture
def sagepayment_tva(payment, config_request):
    factory = SagePaymentTva(None, config_request)
    factory.set_payment(payment)
    return factory


@pytest.fixture
def sagepayment_remittance(payment, config_request):
    factory = SagePaymentRemittance(None, config_request)
    factory.set_payment(payment)
    return factory


@pytest.mark.payment
class TestSagePaymentMain:
    def test_base_entry(self, sagepayment):
        today = datetime.date.today()
        assert sagepayment.reference == "INV_001/REM_ID"
        assert sagepayment.code_journal == "CODE_JOURNAL_BANK"
        assert sagepayment.date == today
        assert sagepayment.mode == "chèque"
        assert sagepayment.libelle == "company / Rgt customer"

    def test_credit_client(self, sagepayment):
        g_entry, entry = sagepayment.credit_client(10000000)
        assert entry["compte_cg"] == "CG_CUSTOMER"
        assert entry["compte_tiers"] == "CUSTOMER"
        assert entry["credit"] == 10000000

    def test_debit_banque(self, sagepayment):
        g_entry, entry = sagepayment.debit_banque(10000000)
        assert entry["compte_cg"] == "COMPTE_CG_BANK"
        assert entry["debit"] == 10000000


@pytest.mark.payment
class TestSagePaymentTva:
    def test_get_amount(self, sagepayment_tva, dummy_tva_sans_code, payment):
        payment.tva = dummy_tva_sans_code
        sagepayment_tva.set_payment(payment)
        amount = sagepayment_tva.get_amount()
        # tva inversée d'un paiement de 10000000 à 20%
        assert amount == 1666667

    def test_credit_tva(self, sagepayment_tva, dummy_tva_sans_code, payment):
        g_entry, entry = sagepayment_tva.credit_tva(10000000)
        assert entry["credit"] == 10000000
        assert entry["compte_cg"] == "TVAAPAYER0001"
        assert entry["code_taxe"] == "CTVA0001"

        # Test if there is no tva code
        payment.tva = dummy_tva_sans_code
        sagepayment_tva.set_payment(payment)
        g_entry, entry = sagepayment_tva.credit_tva(10000000)
        assert "code_taxe" not in entry

    def test_debit_tva(self, sagepayment_tva):
        g_entry, entry = sagepayment_tva.debit_tva(10000000)
        assert entry["debit"] == 10000000
        assert entry["compte_cg"] == "TVA0001"
        assert entry["code_taxe"] == "CTVA0001"


@pytest.mark.payment
class TestSagePaymentRemittance:
    def test_debit_banque(self, sagepayment_remittance, payment):
        g_entry, entry = sagepayment_remittance.debit_banque()
        assert entry["debit"] == payment.amount  # 10000000
        assert entry["compte_cg"] == "COMPTE_CG_BANK"
        assert entry["reference"] == "REM_ID"


@pytest.mark.payment
class TestInternalSagePaymentMain:
    def test_base_entry(self, internalsagepayment_module):
        today = datetime.date.today()
        assert internalsagepayment_module.reference == "INV_I01"
        assert (
            internalsagepayment_module.code_journal == "INTERNAL_JOURNAL_ENCAISSEMENT"
        )
        assert internalsagepayment_module.date == today
        assert internalsagepayment_module.libelle == "company / Rgt Interne customer"

    def test_credit_client(
        self, dbsession, internalsagepayment_module, customer, company
    ):
        g_entry, entry = internalsagepayment_module.credit_client(95000000)
        assert entry["compte_cg"] == "41100000"
        assert entry["compte_tiers"] == "CUSTOMER"
        assert entry["credit"] == 95000000

        customer.compte_tiers = None
        company.internalthird_party_customer_account = None
        dbsession.merge(company)
        dbsession.flush()
        g_entry, entry = internalsagepayment_module.credit_client(95000000)
        assert entry["compte_tiers"] == "CAE_TIERS_INTERNE"

    def test_debit_banque(self, internalsagepayment_module):
        g_entry, entry = internalsagepayment_module.debit_banque(95000000)
        assert entry["compte_cg"] == "INTERNAL_BANK_CG_ENCAISSEMENT"
        assert entry["debit"] == 95000000


PAYMENT_ITEMS_HEADERS = [
    "reference",
    "code_journal",
    "date",
    "compte_cg",
    "mode",
    "compte_tiers",
    "code_taxe",
    "libelle",
    "debit",
    "credit",
    "type_",
    "num_analytique",
    "_mark_debit_banque",
    "_bank_remittance_id",
]


def build_entries(items_vals):
    """
    Build export entries from a list of values
    """
    items = []
    for raw_entry in items_vals:
        analytic_entry = dict(zip(PAYMENT_ITEMS_HEADERS, raw_entry))
        general_entry = generate_general_entry(analytic_entry)
        items.extend([general_entry, analytic_entry])
    return items


@pytest.fixture
def payment_items():
    # not groupped yet
    items_vals = [
        (
            "2021-43/123456",
            "BQ4",
            "020521",
            "411200",
            "par chèque",
            "NICO",
            "",
            "Arnaud Guillot S.A.R.L. / Rgt Bonne",
            "",
            90,
            "A",
            "ANA-0001",
            False,
            "123456",
        ),
        (
            "2021-43/123456",
            "BQ4",
            "020521",
            "445725",
            "par chèque",
            "",
            "V20",
            "Arnaud Guillot S.A.R.L. / Rgt Bonne",
            "",
            15,
            "A",
            "ANA-0001",
            False,
            "123456",
        ),
        (
            "2021-43/123456",
            "BQ4",
            "020521",
            "445715",
            "par chèque",
            "",
            "V20",
            "Arnaud Guillot S.A.R.L. / Rgt Bonne",
            15,
            "",
            "A",
            "ANA-0001",
            False,
            "123456",
        ),
        (
            "123456",
            "BQ4",
            "040521",
            "512150",
            "par chèque",
            "",
            "",
            "Remise 123456",
            90,
            "",
            "A",
            "ANA-0001",
            True,
            "123456",
        ),
        (
            "2021-42/123456",
            "BQ4",
            "040521",
            "411200",
            "par chèque",
            "BRED",
            "",
            "Andre Barthelemy SA / Rgt Benoit Cl",
            "",
            252,
            "A",
            "ANA-0002",
            False,
            "123456",
        ),
        (
            "2021-42/123456",
            "BQ4",
            "040521",
            "445725",
            "par chèque",
            "",
            "V20",
            "Andre Barthelemy SA / Rgt Benoit Cl",
            "",
            42,
            "A",
            "ANA-0002",
            False,
            "123456",
        ),
        (
            "2021-42/123456",
            "BQ4",
            "040521",
            "445715",
            "par chèque",
            "",
            "V20",
            "Andre Barthelemy SA / Rgt Benoit Cl",
            42,
            "",
            "A",
            "ANA-0002",
            False,
            "123456",
        ),
        (
            "123456",
            "BQ4",
            "040521",
            "512150",
            "par chèque",
            "",
            "",
            "Remise 123456",
            252,
            "",
            "A",
            "ANA-0002",
            True,
            "123456",
        ),
    ]
    return build_entries(items_vals)


def _check_includes(expected_lines, lines):
    """
    teste si le contenu des expected_lines est bien présent dans lines
    """
    for line in lines:
        line.pop("_analytic_counterpart", None)
        line.pop("_general_counterpart", None)

    for index, item in enumerate(expected_lines):
        line = lines[index]
        # On supprime les colonnes num_analytique car elles ne sont pas produites
        # par l'export mais le sont dans le test
        if item["type_"] == "G":
            item.pop("num_analytique", None)

        for key, value in item.items():
            assert line[key] == value


def get_export_groupper(get_csrf_request_with_db):
    return PaymentExportGroupper(None, get_csrf_request_with_db())


def test_payment_export_groupper_strategy_none(
    mk_config, payment_items, get_csrf_request_with_db
):
    mk_config("receipts_grouping_strategy", "")
    groupper_disabled = get_export_groupper(get_csrf_request_with_db)

    assert groupper_disabled.group_items(payment_items) == payment_items


def test_payment_export_groupper_strategy_remittance_id(
    mk_config, payment_items, get_csrf_request_with_db
):
    mk_config("receipts_grouping_strategy", "remittance_id")
    groupper_enabled = get_export_groupper(get_csrf_request_with_db)
    groupped_items = groupper_enabled.group_items(payment_items)
    expected = [
        dict(zip(PAYMENT_ITEMS_HEADERS, line))
        for line in [
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "411200",
                "par chèque",
                "NICO",
                "",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                90,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "411200",
                "par chèque",
                "NICO",
                "",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                90,
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                15,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                15,
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                15,
                "",
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                15,
                "",
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            (
                "123456",
                "BQ4",
                "040521",
                "512150",
                "par chèque",
                "",
                "",
                "Remise 123456",
                342,
                "",
                "G",
                "",
                True,
                "123456",
            ),
            (
                "123456",
                "BQ4",
                "040521",
                "512150",
                "par chèque",
                "",
                "",
                "Remise 123456",
                342,
                "",
                "A",
                "* DIVERS *",
                True,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "411200",
                "par chèque",
                "BRED",
                "",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                252,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "411200",
                "par chèque",
                "BRED",
                "",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                252,
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                42,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                42,
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                42,
                "",
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                42,
                "",
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
        ]
    ]
    _check_includes(expected, groupped_items)


def test_payment_export_groupper_strategy_remittance_id_code_analytique(
    mk_config,
    payment_items,
    get_csrf_request_with_db,
):
    mk_config("receipts_grouping_strategy", "remittance_id+code_analytique")
    groupper_enabled = get_export_groupper(get_csrf_request_with_db)
    # No entry with same analytic AND remittance id
    groupped_items = groupper_enabled.group_items(payment_items)
    expected = [
        dict(zip(PAYMENT_ITEMS_HEADERS, line))
        for line in [
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "411200",
                "par chèque",
                "NICO",
                "",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                90,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "411200",
                "par chèque",
                "NICO",
                "",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                90,
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                15,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                "",
                15,
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                15,
                "",
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-43/123456",
                "BQ4",
                "020521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Arnaud Guillot S.A.R.L. / Rgt Bonne",
                15,
                "",
                "A",
                "ANA-0001",
                False,
                "123456",
            ),
            # We did group general line:
            (
                "123456",
                "BQ4",
                "040521",
                "512150",
                "par chèque",
                "",
                "",
                "Remise 123456",
                342,
                "",
                "G",
                "",
                True,
                "123456",
            ),
            # We did not group analytical line (different num analytic):
            (
                "123456",
                "BQ4",
                "040521",
                "512150",
                "par chèque",
                "",
                "",
                "Remise 123456",
                90,
                "",
                "A",
                "ANA-0001",
                True,
                "123456",
            ),
            # We did not group analytical line (different num analytic):
            (
                "123456",
                "BQ4",
                "040521",
                "512150",
                "par chèque",
                "",
                "",
                "Remise 123456",
                252,
                "",
                "A",
                "ANA-0002",
                True,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "411200",
                "par chèque",
                "BRED",
                "",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                252,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "411200",
                "par chèque",
                "BRED",
                "",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                252,
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                42,
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445725",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                "",
                42,
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                42,
                "",
                "G",
                "",
                False,
                "123456",
            ),
            (
                "2021-42/123456",
                "BQ4",
                "040521",
                "445715",
                "par chèque",
                "",
                "V20",
                "Andre Barthelemy SA / Rgt Benoit Cl",
                42,
                "",
                "A",
                "ANA-0002",
                False,
                "123456",
            ),
        ]
    ]
    _check_includes(expected, groupped_items)


@pytest.fixture
def mk_payments():
    payment_defaults = dict(
        zip(
            PAYMENT_ITEMS_HEADERS,
            (
                "1103448908",
                "CE",
                "150322",
                "51220000",
                "Espèces",
                "NICO",
                "",
                "Remise 12341234",
                100000,
                "",
                "A",
                "",
                True,
                "12341234",
            ),
        )
    )

    def _mk_two_payments(payments: Iterable[dict]):
        for payment_props in payments:
            payment = payment_defaults.copy()
            payment.update(payment_props)

            # Simulate real-life example where key is not pointing
            # something empty, but key is missing.
            for k in ["debit", "credit"]:
                if payment[k] == "":
                    del payment[k]
            yield generate_general_entry(payment)
            yield payment

    return _mk_two_payments


def test_payment_export_groupper_negative_payment(
    mk_config, mk_payments, get_csrf_request_with_db
):
    """
    Bug #3419 : le multi-tva sépare un paiement saisi en plusieurs (un par taux de TVA)

    Si on a des lignes négatives dans la facture,
    on peut parvenir à un paiement d'un montant négatif.
    """
    mk_config("receipts_grouping_strategy", "remittance_id")
    groupper_enabled = get_export_groupper(get_csrf_request_with_db)

    payment_items = mk_payments(
        [
            {"credit": "", "debit": 100000},
            {"credit": 8000, "debit": ""},
        ]
    )

    groupped_items = list(groupper_enabled.group_items(payment_items))

    assert len(groupped_items) == 2
    assert groupped_items[0]["debit"] == 100000 - 8000
    assert not groupped_items[0]["credit"]
