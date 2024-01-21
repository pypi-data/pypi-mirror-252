"""
Test admin form tools
"""
import pytest
import colander


def test_invoice_number_template_validator():
    from endi.forms.admin import get_number_template_validator
    from endi.models.task.services import InvoiceNumberService

    invoice_number_template_validator = get_number_template_validator(
        InvoiceNumberService
    )
    # Ref https://framagit.org/endi/endi/issues/1086
    with pytest.raises(colander.Invalid):
        invoice_number_template_validator(None, "2018-{SEQYEAR}")

    assert invoice_number_template_validator(None, "2018-{SEQGLOBAL}") is None
