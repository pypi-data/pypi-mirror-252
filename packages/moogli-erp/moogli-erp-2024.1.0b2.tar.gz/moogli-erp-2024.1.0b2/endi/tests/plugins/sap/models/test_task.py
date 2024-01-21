import pytest

pytestmark = [pytest.mark.plugin_sap]


def test_invoice_options_forcing(mk_invoice, invoice, dbsession):

    # Create
    invoice = mk_invoice(display_ttc=False, display_units=False)
    assert invoice.display_ttc == True  # noqa
    assert invoice.display_ttc == True  # noqa

    # Edit
    invoice.display_ttc = False
    invoice.display_units = False
    dbsession.merge(invoice)
    dbsession.flush()
    assert invoice.display_ttc == True  # noqa
    assert invoice.display_units == True  # noqa
