import pytest


@pytest.fixture
def task_line(mk_task_line, task_line_group):
    return mk_task_line(cost=12500000, group=task_line_group)


@pytest.fixture
def payment_line(mk_payment_line):
    return mk_payment_line(amount=12500000)


@pytest.fixture
def populated_invoice(dbsession, invoice, task_line_group, task_line):
    invoice.line_groups = [task_line_group]
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    return invoice
