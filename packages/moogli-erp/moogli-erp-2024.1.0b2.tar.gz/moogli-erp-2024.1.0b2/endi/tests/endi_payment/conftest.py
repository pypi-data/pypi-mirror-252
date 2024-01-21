import pytest


@pytest.fixture
def product_without_tva(dbsession):
    from endi.models.tva import Product

    product = Product(name="product", compte_cg="122")
    dbsession.add(product)
    dbsession.flush()
    return product


@pytest.fixture
def task_line_group(dbsession):
    from endi.models.task.task import TaskLineGroup

    group = TaskLineGroup(
        order=1,
        title="Group title",
        description="Group description",
    )
    dbsession.add(group)
    dbsession.flush()
    return group


@pytest.fixture
def task_line(dbsession, unity, tva, product, task_line_group):
    from endi.models.task.task import TaskLine

    # TTC = 120 €
    line = TaskLine(
        cost=10000000,
        quantity=1,
        unity=unity.label,
        tva=tva.value,
        product_id=product.id,
        group=task_line_group,
    )
    dbsession.add(line)
    dbsession.flush()
    return line


@pytest.fixture
def discount_line(dbsession, tva):
    from endi.models.task.task import DiscountLine

    discount = DiscountLine(description="Discount", amount=1000000, tva=tva.value)
    dbsession.add(discount)
    dbsession.flush()
    return discount


@pytest.fixture
def invoice(mk_invoice):
    return mk_invoice(date=None, pdf_file_hash="pdf file hash")


@pytest.fixture
def full_invoice(
    dbsession,
    invoice,
    task_line_group,
    task_line,
    user,
    mention,
    discount_line,
    date_20190101,
):
    # TTC  : 120 - 12  + 12 €
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    invoice.discounts = [discount_line]
    invoice.workplace = "workplace"
    invoice.mentions = [mention]
    invoice.expenses_ht = 1000000
    invoice.start_date = date_20190101
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def bank_remittance(dbsession, bank, user, mode):
    from endi.models.task.payment import BankRemittance

    remittance = BankRemittance(
        id="REM_ID",
        payment_mode=mode.label,
        bank_id=bank.id,
        remittance_date="2019-01-01",
        closed=1,
    )
    dbsession.add(remittance)
    dbsession.flush()
    return remittance


@pytest.fixture
def payment(dbsession, bank, full_invoice, user, mode, bank_remittance, customer_bank):
    from endi.models.task.payment import Payment

    payment = Payment(
        amount=15 * 10**5,
        bank_id=bank.id,
        user_id=user.id,
        task_id=full_invoice.id,
        bank_remittance_id=bank_remittance.id,
        mode=mode.label,
        customer_bank_id=customer_bank.id,
        check_number="0123456789",
        issuer=full_invoice.customer.label,
    )
    dbsession.add(payment)
    dbsession.flush()
    return payment


@pytest.fixture
def mk_payment_history(dbsession, fixture_factory):
    from endi_payment.models import EndiPaymentHistory
    import datetime

    return fixture_factory(
        EndiPaymentHistory,
        created_at=datetime.datetime.now(),
        date=datetime.date.today(),
        invoice_id=1,
        payment_id=1,
        invoice_pdf_file_hash="pdf file hash",
        tva_value=2000,
        amount=100000,
        previous_entry_hash="",
        user_login="test@test.fr",
    )


@pytest.fixture(autouse=True)
def endi_payment_setup(config, connection):
    from endi_base.models.base import DBSESSION

    config.include("endi_payment")
