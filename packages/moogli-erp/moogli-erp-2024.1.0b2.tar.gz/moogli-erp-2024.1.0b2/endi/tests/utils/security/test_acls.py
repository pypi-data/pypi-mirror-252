import pytest
import datetime
from endi.utils.security.acls import get_estimation_default_acl, get_invoice_default_acl
from endi.tests.tools import (
    Dummy,
    check_acl,
)
from endi.models.task import (
    TaskLineGroup,
)


@pytest.fixture
def company(mk_company):
    return mk_company(id=1)


@pytest.fixture
def dummy_project():
    project_type = Dummy(default=True, with_business=False)
    project = Dummy(project_type=project_type, company_id=1)
    return project


@pytest.fixture
def estimation(mk_estimation, mk_project, mk_project_type, company):
    project_type = mk_project_type(name="default", with_business=False)
    project = mk_project(project_type=project_type, company=company)
    return mk_estimation(
        status="draft",
        company=company,
        signed_status="waiting",
        geninv=False,
        type_="estimation",
        project=project,
        internal=False,
    )


@pytest.fixture
def invoice(
    dbsession,
    mk_invoice,
    mk_project,
    mk_project_type,
    company,
    task_line,
    task_line_group,
):
    inv = mk_invoice(
        status="draft",
        paid_status="waiting",
        exported=False,
        invoicing_mode="classic",
        internal=False,
        supplier_invoice_id=None,
        company=company,
    )
    inv.line_groups = [task_line_group]
    inv = dbsession.merge(inv)
    dbsession.flush()
    return inv


@pytest.fixture
def estimation_exceed_limit_amount(dbsession, mk_task_line, estimation):
    line = mk_task_line(
        tva=200, cost=20000000, description="Product line"  # 200 euros HT
    )
    estimation.line_groups = [TaskLineGroup(lines=[line])]
    dbsession.merge(estimation)
    dbsession.flush()
    return estimation


@pytest.fixture
def invoice_exceed_limit_amount(dbsession, mk_task_line, invoice):
    line = mk_task_line(
        tva=200, cost=20000000, description="Product line"  # 200 euros HT
    )
    invoice.line_groups = [TaskLineGroup(lines=[line])]
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def internalinvoice(mk_internalinvoice, mk_project, mk_project_type, company):
    return mk_internalinvoice(
        status="draft",
        company=company,
        paid_status="waiting",
        exported=False,
        invoicing_mode="classic",
        CLASSIC_MODE="classic",
        internal=True,
        supplier_invoice_id=None,
    )


@pytest.fixture
def cancelinvoice():
    return Dummy(
        status="draft",
        company_id=1,
        exported=False,
        type_="cancelinvoice",
        internal=False,
    )


@pytest.fixture
def expense_sheet():
    return Dummy(
        status="draft",
        company_id=1,
        paid_status="waiting",
        expense_exported=False,
        purchase_exported=False,
        type_="expensesheet",
    )


@pytest.fixture
def supplier_order_exceed_limit_amount(
    dbsession,
    mk_supplier_order_line,
    company,
    supplier_order,
):
    line = mk_supplier_order_line(
        description="Commande fournisseur",
        ht=10000000,
        tva=100,
        supplier_order=supplier_order,
    )
    supplier_order.lines = [line]
    dbsession.merge(supplier_order)
    dbsession.flush()
    return supplier_order


@pytest.fixture
def supplier_invoice_exceed_limit_amount(
    dbsession,
    mk_supplier_invoice_line,
    company,
    supplier_invoice,
):
    line = mk_supplier_invoice_line(
        description="Facture fournisseur",
        ht=10000000,
        tva=100,
        supplier_invoice=supplier_invoice,
    )
    supplier_invoice.lines = [line]
    dbsession.merge(supplier_invoice)
    dbsession.flush()
    return supplier_invoice


@pytest.fixture
def acl_request(get_csrf_request, user):
    return get_csrf_request(user=user)


def test_supplier_order(
    supplier_order, supplier_order_exceed_limit_amount, acl_request, user
):
    from endi.utils.security.acls import get_supplier_order_default_acl

    # Draft acls
    acl = get_supplier_order_default_acl(supplier_order)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Wait acls
    supplier_order.status = "wait"
    acl = get_supplier_order_default_acl(supplier_order)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Invalid acls
    supplier_order.status = "invalid"
    acl = get_supplier_order_default_acl(supplier_order)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Valid acls
    supplier_order.status = "valid"
    acl = get_supplier_order_default_acl(supplier_order)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert not check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")


def test_supplier_order_exceed_limit_amount(
    supplier_order_exceed_limit_amount, acl_request, login, user
):
    from endi.utils.security.acls import get_supplier_order_default_acl

    login.supplier_order_limit_amount = 100

    # Draft acls and invoice amount > supplier_order_limit_amount

    acl = get_supplier_order_default_acl(supplier_order_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert not check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Wait acls  and invoice amount > supplier_order_limit_amount
    supplier_order_exceed_limit_amount.status = "wait"
    acl = get_supplier_order_default_acl(supplier_order_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert not check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Invalid acls and invoice amount > supplier_order_limit_amount
    supplier_order_exceed_limit_amount.status = "invalid"
    acl = get_supplier_order_default_acl(supplier_order_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert not check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")

    # Valid acls and invoice amount > supplier_order_limit_amount
    supplier_order_exceed_limit_amount.status = "valid"
    acl = get_supplier_order_default_acl(supplier_order_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_order", "company:1")
    assert not check_acl(acl, "valid.supplier_order", "group:supplier_order_validation")


def test_supplier_invoice(supplier_invoice, acl_request, user):
    from endi.utils.security.acls import get_supplier_invoice_acl

    # Draft acls
    acl = get_supplier_invoice_acl(supplier_invoice)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Wait acls
    supplier_invoice.status = "wait"
    acl = get_supplier_invoice_acl(supplier_invoice)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Invalid acls
    supplier_invoice.status = "invalid"
    acl = get_supplier_invoice_acl(supplier_invoice)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Valid acls
    supplier_invoice.status = "valid"
    acl = get_supplier_invoice_acl(supplier_invoice)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert not check_acl(
        acl, "valid.supplier_invoice", "group:supplier_invoice_validation"
    )


def test_supplier_invoice_exceed_limit_amount(
    supplier_invoice_exceed_limit_amount, acl_request, user, login
):
    from endi.utils.security.acls import get_supplier_invoice_acl

    login.supplier_order_limit_amount = 100

    # Draft acls
    acl = get_supplier_invoice_acl(supplier_invoice_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Wait acls
    supplier_invoice_exceed_limit_amount.status = "wait"
    acl = get_supplier_invoice_acl(supplier_invoice_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Invalid acls
    supplier_invoice_exceed_limit_amount.status = "invalid"
    acl = get_supplier_invoice_acl(supplier_invoice_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert check_acl(acl, "valid.supplier_invoice", "group:supplier_invoice_validation")

    # Valid acls
    supplier_invoice_exceed_limit_amount.status = "valid"
    acl = get_supplier_invoice_acl(supplier_invoice_exceed_limit_amount)
    assert not check_acl(acl, "valid.supplier_invoice", "company:1")
    assert not check_acl(
        acl, "valid.supplier_invoice", "group:supplier_invoice_validation"
    )


def test_estimation_default_acls(estimation, acl_request, user):
    # Draft acls
    acl = get_estimation_default_acl(estimation)
    # User
    for ace in (
        "wait.estimation",
        "edit.estimation",
        "delete.estimation",
        "draft.estimation",
        "add.file",
        "view.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.estimation", "company:1")

    assert not check_acl(acl, "geninv.estimation", "company:1")
    assert not check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        for ace in (
            "edit.estimation",
            "delete.estimation",
            "draft.estimation",
            "add.file",
            "view.file",
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.estimation", group)
        assert check_acl(acl, "wait.estimation", group)

        assert not check_acl(acl, "geninv.estimation", group)
        assert not check_acl(acl, "set_signed_status.estimation", group)

    # Auto validation draft status
    assert check_acl(acl, "valid.estimation", "group:estimation_validation")
    assert check_acl(acl, "edit.estimation", "group:estimation_validation")

    # Invalid acls
    estimation.status = "invalid"
    acl = get_estimation_default_acl(estimation)
    # User
    for ace in (
        "wait.estimation",
        "edit.estimation",
        "delete.estimation",
        "draft.estimation",
        "add.file",
        "view.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.estimation", "company:1")

    assert not check_acl(acl, "geninv.estimation", "company:1")
    assert not check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins && groups
    for group in ("group:admin", "group:manager"):
        for ace in (
            "edit.estimation",
            "delete.estimation",
            "draft.estimation",
            "add.file",
            "view.file",
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.estimation", group)
        assert check_acl(acl, "wait.estimation", group)

        assert not check_acl(acl, "geninv.estimation", group)
        assert not check_acl(acl, "set_signed_status.estimation", group)

    # Auto validation invalid status
    assert check_acl(acl, "valid.estimation", "group:estimation_validation")
    assert check_acl(acl, "edit.estimation", "group:estimation_validation")

    # Wait acls
    estimation.status = "wait"
    acl = get_estimation_default_acl(estimation)
    # #  User
    assert check_acl(acl, "draft.estimation", "company:1")
    assert not check_acl(acl, "wait.estimation", "company:1")
    assert not check_acl(acl, "edit.estimation", "company:1")
    assert not check_acl(acl, "valid.estimation", "company:1")

    assert not check_acl(acl, "set_date.estimation", "company:1")
    assert not check_acl(acl, "geninv.estimation", "company:1")
    assert not check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "valid.estimation", group)
        assert check_acl(acl, "invalid.estimation", group)
        assert check_acl(acl, "edit.estimation", group)
        assert check_acl(acl, "delete.estimation", group)
        assert check_acl(acl, "draft.estimation", "company:1")
        assert not check_acl(acl, "geninv.estimation", group)
        assert not check_acl(acl, "set_signed_status.estimation", group)

    # Auto validation wait status
    assert check_acl(acl, "valid.estimation", "group:estimation_validation")
    assert check_acl(acl, "edit.estimation", "group:estimation_validation")

    # Valid acls
    estimation.status = "valid"
    acl = get_estimation_default_acl(estimation)
    # # User
    assert not check_acl(acl, "edit.estimation", "company:1")
    assert not check_acl(acl, "delete.estimation", "company:1")

    assert not check_acl(acl, "set_date.estimation", "company:1")
    assert check_acl(acl, "geninv.estimation", "company:1")
    assert check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "edit.estimation", group)
        assert not check_acl(acl, "delete.estimation", group)

        assert check_acl(acl, "set_date.estimation", group)
        assert check_acl(acl, "geninv.estimation", group)
        assert check_acl(acl, "set_signed_status.estimation", group)

    # Aborted acls
    estimation.signed_status = "aborted"

    acl = get_estimation_default_acl(estimation)
    # # User
    assert not check_acl(acl, "geninv.estimation", "company:1")
    assert check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "geninv.estimation", group)
        assert check_acl(acl, "set_signed_status.estimation", group)

    # Auto validation valid status
    assert not check_acl(acl, "valid.estimation", "group:estimation_validation")
    assert not check_acl(acl, "edit.estimation", "group:estimation_validation")

    # Signed acls
    estimation.signed_status = "signed"
    acl = get_estimation_default_acl(estimation)
    # # User
    assert check_acl(acl, "geninv.estimation", "company:1")
    assert check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "geninv.estimation", group)
        assert check_acl(acl, "set_signed_status.estimation", group)
        assert not check_acl(acl, "set_date.estimation", group)

    # geninv acls
    estimation.signed_status = "waiting"
    estimation.geninv = True
    acl = get_estimation_default_acl(estimation)
    # # User
    assert check_acl(acl, "geninv.estimation", "company:1")
    assert check_acl(acl, "set_signed_status.estimation", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "geninv.estimation", group)
        assert check_acl(acl, "set_signed_status.estimation", group)
        assert not check_acl(acl, "set_date.estimation", group)


def test_estimation_exceed_limit_amount(
    estimation_exceed_limit_amount, acl_request, user, login
):
    login.estimation_limit_amount = 100.0

    estimation_exceed_limit_amount.status = "draft"
    acl = get_estimation_default_acl(estimation_exceed_limit_amount)

    assert check_acl(acl, "edit.estimation", "group:estimation_validation")
    assert not check_acl(acl, "valid.estimation", "group:estimation_validation")

    estimation_exceed_limit_amount.status = "invalid"
    acl = get_estimation_default_acl(estimation_exceed_limit_amount)

    assert check_acl(acl, "edit.estimation", "group:estimation_validation")
    assert not check_acl(acl, "valid.estimation", "group:estimation_validation")

    estimation_exceed_limit_amount.status = "wait"
    acl = get_estimation_default_acl(estimation_exceed_limit_amount)

    assert check_acl(acl, "edit.estimation", "group:estimation_validation")
    assert not check_acl(acl, "valid.estimation", "group:estimation_validation")

    estimation_exceed_limit_amount.status = "valid"
    acl = get_estimation_default_acl(estimation_exceed_limit_amount)

    assert not check_acl(acl, "edit.estimation", "group:estimation_validation")
    assert not check_acl(acl, "valid.estimation", "group:estimation_validation")


def test_invoice_default_acls(invoice, acl_request):
    # Draft acls
    acl = get_invoice_default_acl(invoice)
    # User
    # status related acl
    for ace in (
        "wait.invoice",
        "edit.invoice",
        "delete.invoice",
        "view.file",
        "add.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.invoice", "company:1")
    # specific acl
    assert not check_acl(acl, "gencinv.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")

    # Admins
    for group in ("group:admin", "group:manager"):
        for ace in ("edit.invoice", "delete.invoice", "view.file", "add.file"):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.invoice", group)
        assert check_acl(acl, "wait.invoice", group)
        assert not check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
    assert check_acl(acl, "valid.invoice", "group:invoice_validation")

    # Auto validation draft status
    assert check_acl(acl, "valid.invoice", "group:invoice_validation")
    assert check_acl(acl, "edit.invoice", "group:invoice_validation")

    # Wait acls
    invoice.status = "wait"
    acl = get_invoice_default_acl(invoice)
    # #  User
    assert check_acl(acl, "view.invoice", "company:1")
    assert not check_acl(acl, "edit.invoice", "company:1")
    assert not check_acl(acl, "set_date.invoice", "company:1")
    assert not check_acl(acl, "gencinv.invoice")
    assert not check_acl(acl, "valid.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "edit.invoice", group)
        assert check_acl(acl, "delete.invoice", group)
        assert check_acl(acl, "valid.invoice", group)
        assert not check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Auto validation wait status
    assert check_acl(acl, "valid.invoice", "group:invoice_validation")
    assert check_acl(acl, "edit.invoice", "group:invoice_validation")

    # Valid acls
    invoice.status = "valid"

    acl = get_invoice_default_acl(invoice)
    # # User
    assert not check_acl(acl, "edit.invoice", "company:1")
    assert not check_acl(acl, "set_date.invoice", "company:1")
    assert not check_acl(acl, "delete.invoice", "company:1")
    assert check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "view.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")
    assert check_acl(acl, "add_payment.invoice", "group:payment_admin")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "edit.invoice", group)
        assert not check_acl(acl, "delete.invoice", group)
        assert check_acl(acl, "view.invoice", group)
        assert check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Auto validation valid status
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")
    assert not check_acl(acl, "edit.invoice", "group:invoice_validation")

    # Paid acls
    invoice.paid_status = "paid"

    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")
    assert check_acl(acl, "add_payment.invoice", "group:payment_admin")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add_payment.invoice", group)
        assert not check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Resulted acls
    invoice.paid_status = "resulted"
    acl = get_invoice_default_acl(invoice)
    # # User
    assert not check_acl(acl, "gencinv.invoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
        assert not check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "add.file", group)

    # exported acls
    invoice.paid_status = "waiting"
    invoice.exported = True
    acl = get_invoice_default_acl(invoice)
    # # User
    assert check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")
    assert check_acl(acl, "add_payment.invoice", "group:payment_admin")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add_payment.invoice", group)
        assert check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "set_treasury.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Auto validation wait status
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")
    assert not check_acl(acl, "edit.invoice", "group:invoice_validation")


def test_invoice_exceed_limit_amount(invoice_exceed_limit_amount, acl_request, login):
    login.invoice_limit_amount = 100.0

    invoice_exceed_limit_amount.status = "draft"
    acl = get_invoice_default_acl(invoice_exceed_limit_amount)

    assert check_acl(acl, "edit.invoice", "group:invoice_validation")
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")

    invoice_exceed_limit_amount.status = "invalid"
    acl = get_invoice_default_acl(invoice_exceed_limit_amount)

    assert check_acl(acl, "edit.invoice", "group:invoice_validation")
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")

    invoice_exceed_limit_amount.status = "wait"
    acl = get_invoice_default_acl(invoice_exceed_limit_amount)

    assert check_acl(acl, "edit.invoice", "group:invoice_validation")
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")

    invoice_exceed_limit_amount.status = "valid"
    acl = get_invoice_default_acl(invoice_exceed_limit_amount)

    assert not check_acl(acl, "edit.invoice", "group:invoice_validation")
    assert not check_acl(acl, "valid.invoice", "group:invoice_validation")


def test_internalinvoice_default_acls(internalinvoice, acl_request):
    from endi.utils.security.acls import get_invoice_default_acl

    # Draft acls
    acl = get_invoice_default_acl(internalinvoice)
    # User
    # status related acl
    for ace in (
        "wait.invoice",
        "edit.invoice",
        "delete.invoice",
        "view.file",
        "add.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.invoice", "company:1")
    # specific acl
    assert not check_acl(acl, "gencinv.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")
    assert not check_acl(acl, "gen_supplier_invoice.invoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        for ace in ("edit.invoice", "delete.invoice", "view.file", "add.file"):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.invoice", group)
        assert check_acl(acl, "wait.invoice", group)
        assert not check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
    assert check_acl(acl, "valid.invoice", "group:invoice_validation")

    # Wait acls
    internalinvoice.status = "wait"
    acl = get_invoice_default_acl(internalinvoice)
    # #  User
    assert check_acl(acl, "view.invoice", "company:1")
    assert not check_acl(acl, "edit.invoice", "company:1")
    assert not check_acl(acl, "set_date.invoice", "company:1")
    assert not check_acl(acl, "gencinv.invoice")
    assert not check_acl(acl, "valid.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "edit.invoice", group)
        assert check_acl(acl, "delete.invoice", group)
        assert check_acl(acl, "valid.invoice", group)
        assert not check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Valid acls
    internalinvoice.status = "valid"
    acl = get_invoice_default_acl(internalinvoice)
    # # User
    assert not check_acl(acl, "edit.invoice", "company:1")
    assert not check_acl(acl, "set_date.invoice", "company:1")
    assert not check_acl(acl, "delete.invoice", "company:1")
    assert not check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "view.invoice", "company:1")
    assert not check_acl(acl, "add_payment.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    assert not check_acl(acl, "add_payment.invoice", "group:payment_admin")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "edit.invoice", group)
        assert not check_acl(acl, "delete.invoice", group)
        assert check_acl(acl, "view.invoice", group)
        assert check_acl(acl, "set_date.invoice", group)
        assert not check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add.file", group)
        # Ref #3501
        assert not check_acl(acl, "gen_supplier_invoice.invoice", group)

    internalinvoice.status_date -= datetime.timedelta(minutes=2)
    acl = get_invoice_default_acl(internalinvoice)
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "gen_supplier_invoice.invoice", group)

    internalinvoice.supplier_invoice_id = 1
    acl = get_invoice_default_acl(internalinvoice)
    assert not check_acl(acl, "gen_supplier_invoice.invoice", group)

    # Paid acls
    internalinvoice.paid_status = "paid"

    acl = get_invoice_default_acl(internalinvoice)
    # # User
    assert not check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add_payment.invoice", group)
        assert not check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "add.file", group)

    # Resulted acls
    internalinvoice.paid_status = "resulted"
    acl = get_invoice_default_acl(internalinvoice)
    # # User
    assert not check_acl(acl, "gencinv.invoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "gencinv.invoice", group)
        assert not check_acl(acl, "add_payment.invoice", group)
        assert not check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "add.file", group)

    # exported acls
    internalinvoice.paid_status = "waiting"
    internalinvoice.exported = True
    acl = get_invoice_default_acl(internalinvoice)
    # # User
    assert not check_acl(acl, "gencinv.invoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "gencinv.invoice", group)
        assert check_acl(acl, "add_payment.invoice", group)
        assert check_acl(acl, "set_date.invoice", group)
        assert check_acl(acl, "set_treasury.invoice", group)
        assert check_acl(acl, "add.file", group)


def test_cancelinvoice_default_acls(cancelinvoice):
    from endi.utils.security.acls import get_cancelinvoice_default_acl

    # Draft acls
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # User
    # status related acl
    for ace in (
        "wait.cancelinvoice",
        "edit.cancelinvoice",
        "delete.cancelinvoice",
        "view.file",
        "add.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.cancelinvoice", "company:1")
    assert not check_acl(acl, "duplicate.cancelinvoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        for ace in (
            "edit.cancelinvoice",
            "delete.cancelinvoice",
            "view.file",
            "add.file",
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.cancelinvoice", group)
        assert check_acl(acl, "wait.cancelinvoice", group)
    assert not check_acl(acl, "valid.cancelinvoice", "group:invoice_validation")
    assert check_acl(acl, "valid.cancelinvoice", "group:cancelinvoice_validation")

    assert not check_acl(acl, "duplicate.cancelinvoice", group)

    # Wait acls
    cancelinvoice.status = "wait"
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # #  User
    assert check_acl(acl, "view.cancelinvoice", "company:1")
    assert not check_acl(acl, "edit.cancelinvoice", "company:1")
    assert not check_acl(acl, "set_date.cancelinvoice", "company:1")
    assert not check_acl(acl, "valid.cancelinvoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")
    assert not check_acl(acl, "duplicate.cancelinvoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "edit.cancelinvoice", group)
        assert check_acl(acl, "delete.cancelinvoice", group)
        assert check_acl(acl, "valid.cancelinvoice", group)
        assert check_acl(acl, "add.file", group)
        assert not check_acl(acl, "duplicate.cancelinvoice", group)

    # Valid acls
    cancelinvoice.status = "valid"
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # # User
    assert not check_acl(acl, "edit.cancelinvoice", "company:1")
    assert not check_acl(acl, "set_date.cancelinvoice", "company:1")
    assert not check_acl(acl, "delete.cancelinvoice", "company:1")
    assert check_acl(acl, "view.cancelinvoice", "company:1")
    assert check_acl(acl, "add.file", "company:1")
    assert not check_acl(acl, "duplicate.cancelinvoice", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "edit.cancelinvoice", group)
        assert not check_acl(acl, "delete.cancelinvoice", group)
        assert check_acl(acl, "view.cancelinvoice", group)
        assert check_acl(acl, "set_date.cancelinvoice", group)
        assert check_acl(acl, "add.file", group)
        assert not check_acl(acl, "duplicate.cancelinvoice", group)

    # exported acls
    cancelinvoice.exported = True
    acl = get_cancelinvoice_default_acl(cancelinvoice)
    # # User

    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "set_date.cancelinvoice", group)
        assert check_acl(acl, "set_treasury.cancelinvoice", group)
        assert check_acl(acl, "add.file", group)


def test_expense_sheet_default_acls(expense_sheet):
    from endi.utils.security.acls import get_expense_sheet_default_acl

    acl = get_expense_sheet_default_acl(expense_sheet)

    # User
    # status related acl
    for ace in (
        "wait.expensesheet",
        "edit.expensesheet",
        "delete.expensesheet",
        "view.file",
        "add.file",
    ):
        assert check_acl(acl, ace, "company:1")
    assert not check_acl(acl, "valid.expensesheet", "company:1")
    # specific acl
    assert not check_acl(acl, "add_payment.expensesheet", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        for ace in (
            "edit.expensesheet",
            "delete.expensesheet",
            "view.file",
            "add.file",
            "wait.expensesheet",
        ):
            assert check_acl(acl, ace, group)

        assert check_acl(acl, "valid.expensesheet", group)
        assert check_acl(acl, "wait.expensesheet", group)
        assert not check_acl(acl, "add_payment.expensesheet", group)

    # Wait acls
    expense_sheet.status = "wait"
    acl = get_expense_sheet_default_acl(expense_sheet)
    # #  User
    assert check_acl(acl, "view.expensesheet", "company:1")
    assert not check_acl(acl, "edit.expensesheet", "company:1")
    assert not check_acl(acl, "valid.expensesheet", "company:1")
    assert not check_acl(acl, "add_payment.expensesheet", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "edit.expensesheet", group)
        assert check_acl(acl, "delete.expensesheet", group)
        assert check_acl(acl, "valid.expensesheet", group)
        assert check_acl(acl, "set_justified.expensesheet", group)
        assert not check_acl(acl, "add_payment.expensesheet", group)
        assert check_acl(acl, "add.file", group)

    # Valid acls
    expense_sheet.status = "valid"
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert not check_acl(acl, "edit.expensesheet", "company:1")
    assert not check_acl(acl, "delete.expensesheet", "company:1")
    assert check_acl(acl, "view.expensesheet", "company:1")
    assert not check_acl(acl, "add_payment.expensesheet", "company:1")
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "edit.expensesheet", group)
        assert not check_acl(acl, "delete.expensesheet", group)
        assert check_acl(acl, "view.expensesheet", group)
        assert check_acl(acl, "add.file", group)

    # Paid acls
    expense_sheet.paid_status = "paid"

    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "add_payment.expensesheet", group)
        assert check_acl(acl, "add.file", group)

    # Resulted acls
    expense_sheet.paid_status = "resulted"
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert not check_acl(acl, "add_payment.expensesheet", group)
        assert check_acl(acl, "add.file", group)

    # exported acls
    expense_sheet.paid_status = "waiting"
    expense_sheet.expense_exported = True
    expense_sheet.purchase_exported = True
    acl = get_expense_sheet_default_acl(expense_sheet)
    # # User
    assert check_acl(acl, "add.file", "company:1")

    # # Admins
    for group in ("group:admin", "group:manager"):
        assert check_acl(acl, "add_payment.expensesheet", group)
        assert check_acl(acl, "set_treasury.expensesheet", group)
        assert check_acl(acl, "add.file", group)


def test_statuslogentry_acls(mk_status_log_entry, user, login, node):
    from endi.utils.security.acls import get_statuslogentry_acl

    company_id = 42
    node.company_id = company_id

    kwargs = dict(user_id=user.id, node_id=node.id)
    private_sle_acl = get_statuslogentry_acl(
        mk_status_log_entry(visibility="private", **kwargs)
    )
    public_sle_acl = get_statuslogentry_acl(
        mk_status_log_entry(visibility="public", **kwargs)
    )
    manager_sle_acl = get_statuslogentry_acl(
        mk_status_log_entry(visibility="manager", **kwargs)
    )

    view = "view.statuslogentry"
    edit = "edit.statuslogentry"
    delete = "delete.statuslogentry"

    # author
    for acl in (private_sle_acl, public_sle_acl, manager_sle_acl):
        assert check_acl(acl, [view, edit, delete], user.login.login)

    # admin
    for acl in (private_sle_acl, public_sle_acl, manager_sle_acl):
        assert check_acl(acl, [view, edit, delete], "group:admin")

    # manager (EA)
    for acl in (public_sle_acl, manager_sle_acl):
        assert check_acl(acl, view, "group:manager")
        assert not check_acl(acl, [edit, delete], "group:manager")

    assert not check_acl(private_sle_acl, [view, edit, delete], "group:manager")

    # company
    assert check_acl(public_sle_acl, view, f"company:{company_id}")
    assert not check_acl(public_sle_acl, [edit, delete], f"company:{company_id}")
    for acl in (private_sle_acl, manager_sle_acl):
        assert not check_acl(acl, [view, edit, delete], f"company:{company_id}")
