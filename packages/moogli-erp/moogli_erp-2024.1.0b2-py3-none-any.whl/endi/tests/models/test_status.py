import datetime


def tests_status_historization(supplier_order, user):
    from endi.models.status import StatusLogEntry

    supplier_order.status_date = datetime.datetime(2019, 11, 11)
    supplier_order.status_comment = "bla"
    supplier_order.status_user_id = user.id
    supplier_order.status = "draft"
    supplier_order.historize_latest_status("validation_status")

    assert StatusLogEntry.query().count() == 1

    last_entry = StatusLogEntry.query().all()[-1]

    assert last_entry.datetime == datetime.datetime(2019, 11, 11)
    assert last_entry.comment == "bla"
    assert last_entry.user_id == user.id
    assert last_entry.status == "draft"

    supplier_order.status_date = datetime.datetime(2020, 11, 11)
    supplier_order.status_comment = "bli"
    supplier_order.status_user_id = user.id
    supplier_order.status = "valid"
    supplier_order.historize_latest_status("validation_status")

    assert StatusLogEntry.query().count() == 2

    last_entry = StatusLogEntry.query().all()[-1]

    assert last_entry.datetime == datetime.datetime(2020, 11, 11)
    assert last_entry.comment == "bli"
    assert last_entry.user_id == user.id
    assert last_entry.status == "valid"


def test_validation_status_holder_service(
    supplier_order, supplier_invoice, invoiced_supplier_order, dbsession
):
    from endi.models.supply import SupplierOrder, SupplierInvoice
    from endi.models.status import ValidationStatusHolderService

    service = ValidationStatusHolderService()
    query = service.waiting(SupplierOrder, SupplierInvoice)
    assert query.count() == 0

    supplier_order.status = "wait"
    dbsession.merge(supplier_order)
    dbsession.flush()

    query = service.waiting(SupplierOrder, SupplierInvoice)
    assert query.count() == 1

    supplier_invoice.status = "wait"
    dbsession.merge(supplier_invoice)
    dbsession.flush()

    query = service.waiting(SupplierOrder, SupplierInvoice)
    assert query.count() == 2
    assert supplier_order in query
    assert supplier_invoice in query


def test_status_with_emoticons(supplier_order, user):
    from endi.models.status import StatusLogEntry

    supplier_order.status_date = datetime.datetime(2019, 11, 11)
    supplier_order.status_comment = "😀	😁	😂	😃	😄	😅"
    supplier_order.status_user_id = user.id
    supplier_order.status = "draft"
    supplier_order.historize_latest_status("validation_status")

    assert StatusLogEntry.query().count() == 1

    last_entry = StatusLogEntry.query().all()[-1]
    assert last_entry.comment == "😀	😁	😂	😃	😄	😅"
