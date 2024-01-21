import pytest
import datetime

from unittest.mock import MagicMock


@pytest.fixture
def invoice_20170707(mk_invoice):
    return mk_invoice(date=datetime.date(2017, 7, 7))


@pytest.fixture
def invoice_20170808(dbsession, mk_invoice):
    return mk_invoice(date=datetime.date(2017, 7, 7))


@pytest.fixture
def invoice_2018(dbsession, mk_invoice):
    return mk_invoice(date=datetime.date(2018, 7, 7))


@pytest.fixture
def sale_product(dbsession, tva, company):
    from endi.models.sale_product.base import BaseSaleProduct

    s = BaseSaleProduct(
        ht=150000,
        tva=tva,
        company_id=company.id,
        label="Produit du catalogue",
        description="Description du produit du catalogue",
        unity="m",
    )
    dbsession.add(s)
    dbsession.flush()
    return s


@pytest.fixture
def global_seq_1(dbsession, invoice):
    from endi.models.sequence_number import SequenceNumber

    s = SequenceNumber(
        sequence=SequenceNumber.SEQUENCE_INVOICE_GLOBAL,
        index=1,
        node_id=invoice.id,
    )
    dbsession.add(s)
    dbsession.flush()
    return s


@pytest.fixture
def global_seq_2(dbsession, invoice2):
    from endi.models.sequence_number import SequenceNumber

    s = SequenceNumber(
        sequence=SequenceNumber.SEQUENCE_INVOICE_GLOBAL,
        index=2,
        node_id=invoice2.id,
    )
    dbsession.add(s)
    dbsession.flush()
    return s


@pytest.fixture
def set_seq_index(dbsession, mk_invoice, company):
    """Initialize a year seq to a given index"""
    from endi.models.sequence_number import SequenceNumber

    def _set_seq_index(index, year, month, sequence, company=company):
        s = SequenceNumber(
            sequence=sequence,
            index=index,
            node_id=mk_invoice(
                date=datetime.date(year, month, 1),
                company=company,
            ).id,
        )
        dbsession.add(s)
        dbsession.flush()
        return s

    return _set_seq_index


@pytest.fixture
def set_global_seq_index(dbsession, set_seq_index):
    """Initialize the global seq to a given index"""
    from endi.models.sequence_number import SequenceNumber

    def _set_global_seq_index(index):
        return set_seq_index(
            index=index,
            year=2017,
            month=1,
            sequence=SequenceNumber.SEQUENCE_INVOICE_GLOBAL,
        )

    return _set_global_seq_index


@pytest.fixture
def set_year_seq_index(dbsession, set_seq_index):
    """Initialize a year seq to a given index"""
    from endi.models.sequence_number import SequenceNumber

    def _set_year_seq_index(index, year):
        return set_seq_index(
            index=index,
            year=year,
            month=1,
            sequence=SequenceNumber.SEQUENCE_INVOICE_YEAR,
        )

    return _set_year_seq_index


@pytest.fixture
def set_month_seq_index(dbsession, set_seq_index):
    """Initialize a month seq to a given index"""
    from endi.models.sequence_number import SequenceNumber

    def _set_month_seq_index(index, year, month):
        return set_seq_index(
            index=index,
            month=month,
            year=year,
            sequence=SequenceNumber.SEQUENCE_INVOICE_MONTH,
        )

    return _set_month_seq_index


@pytest.fixture
def set_month_company_seq_index(dbsession, set_seq_index):
    """Initialize a month seq to a given index for a given company"""
    from endi.models.sequence_number import SequenceNumber

    def _set_month_company_seq_index(index, year, month, company):
        return set_seq_index(
            index=index,
            month=month,
            year=year,
            sequence=SequenceNumber.SEQUENCE_INVOICE_MONTH_COMPANY,
            company=company,
        )

    return _set_month_company_seq_index


@pytest.fixture
def DummySequence():
    ds = MagicMock()
    ds.get_next_index = MagicMock(return_value=12)
    return ds


@pytest.fixture
def invoice_one(mk_invoice):
    return mk_invoice()


@pytest.fixture
def invoice_two(mk_invoice):
    return mk_invoice()
