import pytest
from pyramid.httpexceptions import HTTPFound
from pyramid_mailer import get_mailer
from endi.views.internal_invoicing.views import (
    generate_order_from_estimation_view,
    generate_supplier_invoice_from_invoice_view,
)


@pytest.fixture
def internalestimation(mk_internalestimation, mk_task_line, task_line_group, dbsession):
    mk_task_line(cost=10000000, tva=0, quantity=1, group=task_line_group)
    e = mk_internalestimation(description="Description", status="valid")
    e.line_groups = [task_line_group]
    dbsession.merge(e)
    dbsession.flush()
    return e


@pytest.fixture
def internalinvoice(mk_internalinvoice, mk_task_line, task_line_group, dbsession):
    mk_task_line(cost=10000000, tva=0, quantity=1, group=task_line_group)
    i = mk_internalinvoice(
        description="Description",
        status="valid",
        official_number="1",
    )
    i.line_groups = [task_line_group]
    dbsession.merge(i)
    dbsession.flush()
    return i


def test_generate_order_from_estimation_view(
    dbsession,
    get_csrf_request_with_db,
    internalestimation,
    config,
):
    config.add_route("/supplier_orders/{id}", "/supplier_orders/{id}")
    config.add_route("/estimations/{id}", "/estimations/{id}")
    request = get_csrf_request_with_db(context=internalestimation)
    mailer = get_mailer(request)
    result = generate_order_from_estimation_view(internalestimation, request)
    assert internalestimation.supplier_order is not None
    assert isinstance(result, HTTPFound)
    assert len(mailer.outbox) == 2


def test_generate_supplier_invoice_from_invoice_view(
    dbsession,
    get_csrf_request_with_db,
    internalinvoice,
    config,
):
    config.add_route("/supplier_invoices/{id}", "/supplier_invoices/{id}")
    config.add_route("/invoices/{id}", "/invoices/{id}")
    request = get_csrf_request_with_db(context=internalinvoice)
    mailer = get_mailer(request)
    result = generate_supplier_invoice_from_invoice_view(internalinvoice, request)
    assert internalinvoice.supplier_invoice is not None
    assert (
        internalinvoice.supplier_invoice.remote_invoice_number
        == internalinvoice.official_number
    )
    assert isinstance(result, HTTPFound)
    assert len(mailer.outbox) == 2
