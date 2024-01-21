from endi.models.third_party.customer import Customer
from endi.views.third_party.customer.views import (
    customer_delete,
    customer_archive,
)


def test_customer_delete(customer, get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    cid = customer.id
    req.context = customer
    req.referer = "/"
    customer_delete(req)
    req.dbsession.flush()
    assert Customer.get(cid) is None


def test_customer_archive(customer, get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    cid = customer.id
    req.context = customer
    req.referer = "/"
    customer_archive(req)
    req.dbsession.flush()
    assert Customer.get(cid).archived
    customer_archive(req)
    req.dbsession.flush()
    assert Customer.get(cid).archived is False
