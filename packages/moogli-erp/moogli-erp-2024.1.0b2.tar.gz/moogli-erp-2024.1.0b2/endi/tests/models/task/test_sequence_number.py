from datetime import date
from pyramid_retry import RetryableException

import pytest

from endi.models.task.services import InvoiceNumberService
from endi.models.services.official_number import OfficialNumberFormatter


def test_global_invoice_sequence_next_first(global_invoice_sequence, invoice):
    seq_num = global_invoice_sequence.get_next_index(invoice)
    assert seq_num == 1


def test_global_invoice_sequence_next_then(
    global_seq_1,
    global_invoice_sequence,
    invoice,
):
    seq_num = global_invoice_sequence.get_next_index(invoice)
    assert seq_num == 2


def test_global_invoice_sequence_initialization(
    invoice, set_global_seq_index, global_invoice_sequence
):
    from endi.models.config import Config

    Config.set("global_invoice_sequence_init_value", 12)

    assert global_invoice_sequence.get_next_index(invoice) == 13

    # ignore initialization if there is an actual SequenceNumber
    set_global_seq_index(index=20)
    assert global_invoice_sequence.get_next_index(invoice) == 21


def test_year_invoice_sequence(mk_invoice, set_year_seq_index, year_invoice_sequence):
    YIS = year_invoice_sequence

    assert YIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 1
    set_year_seq_index(index=1, year=2017)
    assert YIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 2
    set_year_seq_index(index=2, year=2017)

    assert YIS.get_next_index(mk_invoice(date=date(2018, 2, 1))) == 1
    set_year_seq_index(index=1, year=2018)

    assert YIS.get_next_index(mk_invoice(date=date(2018, 2, 1))) == 2
    set_year_seq_index(index=2, year=2018)

    assert YIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 3


def test_year_invoice_sequence_initialization(
    mk_invoice,
    set_year_seq_index,
    year_invoice_sequence,
):
    YIS = year_invoice_sequence

    from endi.models.config import Config

    Config.set("year_invoice_sequence_init_value", 12)
    Config.set("year_invoice_sequence_init_date", "2017-02-01")

    # year with initialization
    assert YIS.get_next_index(mk_invoice(date=date(2017, 6, 1))) == 13

    # year without initialization
    assert YIS.get_next_index(mk_invoice(date=date(2018, 3, 1))) == 1

    # ignore initialization if there is an actual SequenceNumber
    set_year_seq_index(index=20, year=2017)
    assert YIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 21

    # Falsy year config key ref https://framagit.org/endi/endi/issues/1089
    Config.set("year_invoice_sequence_init_date", "")
    assert YIS.get_next_index(mk_invoice(date=date(2018, 3, 1))) == 1


def test_month_invoice_sequence(
    mk_invoice, month_invoice_sequence, set_month_seq_index
):
    MIS = month_invoice_sequence

    assert MIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 1
    set_month_seq_index(index=1, year=2017, month=1)

    # same year same month
    assert MIS.get_next_index(mk_invoice(date=date(2017, 1, 1))) == 2
    set_month_seq_index(index=2, year=2017, month=1)

    # same year different month
    assert MIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 1
    set_month_seq_index(index=1, year=2017, month=2)

    # same month different year
    assert MIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 1
    set_month_seq_index(index=1, year=2018, month=1)
    assert MIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 2


def test_month_invoice_sequence_initialization(
    mk_invoice,
    month_invoice_sequence,
    set_month_seq_index,
):
    MIS = month_invoice_sequence

    from endi.models.config import Config

    Config.set("month_invoice_sequence_init_value", 12)
    Config.set("month_invoice_sequence_init_date", "2017-02-01")

    # month with initialization
    assert MIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 13

    # month without initialization
    assert MIS.get_next_index(mk_invoice(date=date(2017, 3, 1))) == 1

    # ignore initialization if there is an actual SequenceNumber
    set_month_seq_index(index=20, year=2017, month=2)
    assert MIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 21


def test_month_company_invoice_sequence(
    mk_invoice,
    month_company_invoice_sequence,
    set_month_company_seq_index,
    company,
    company2,
):
    MCIS = month_company_invoice_sequence

    # company
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 1, 1), company=company)) == 1
    set_month_company_seq_index(index=1, year=2017, month=1, company=company)

    # same year same month, company
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 1, 1), company=company)) == 2
    set_month_company_seq_index(index=2, year=2017, month=1, company=company)

    # same year same month, company2
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 1, 1), company=company2)) == 1
    set_month_company_seq_index(index=1, year=2017, month=1, company=company2)

    # same year different month, company
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 2, 1), company=company)) == 1
    set_month_company_seq_index(index=1, year=2017, month=1, company=company)

    # same month different year company
    assert MCIS.get_next_index(mk_invoice(date=date(2018, 1, 1))) == 1


def test_month_company_invoice_sequence_initialization(
    mk_invoice,
    month_company_invoice_sequence,
    set_month_company_seq_index,
    company,
    company2,
    dbsession,
):
    MCIS = month_company_invoice_sequence
    company.month_company_invoice_sequence_init_value = 12
    company.month_company_invoice_sequence_init_date = date(2017, 2, 1)
    dbsession.merge(company)

    # month with initialization
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 13

    # month with initialization, on other company
    assert (
        MCIS.get_next_index(
            mk_invoice(
                date=date(2017, 2, 1),
                company=company2,
            )
        )
        == 1
    )

    # month without initialization
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 3, 1))) == 1

    # ignore initialization if there is an actual SequenceNumber
    set_month_company_seq_index(index=20, year=2017, month=2, company=company)
    assert MCIS.get_next_index(mk_invoice(date=date(2017, 2, 1))) == 21


def test_invoice_number_formatter(invoice_20170707, DummySequence):
    fmt = OfficialNumberFormatter(
        node=invoice_20170707,
        sequences_map={"DUMMY": DummySequence},
    )
    assert fmt.format("") == ""
    assert fmt.format("{YYYY}") == "2017"
    assert fmt.format("{YY}") == "17"
    assert fmt.format("{MM}") == "07"
    assert fmt.format("{ANA}") == "0USER"
    assert fmt.format("{DUMMY}") == "12"
    assert fmt.format("@{DUMMY}-{YYYY}") == "@12-2017"

    with pytest.raises(KeyError):
        assert fmt.format("{DONOTEXIST}")


def test_invoice_number_service_validation():
    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("@{DONOTEXIST}{{SEQGLOBAL}}")

    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("")

    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("aaa")

    # global
    InvoiceNumberService.validate_template("{SEQGLOBAL}-{YYYY}")
    InvoiceNumberService.validate_template("{SEQGLOBAL}")

    # year
    InvoiceNumberService.validate_template("{SEQYEAR}-{YYYY}")
    InvoiceNumberService.validate_template("{SEQYEAR}-{YY}")
    InvoiceNumberService.validate_template("{SEQYEAR}-{SEQMONTH}-{YY}")
    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("{SEQYEAR}")

    # month
    InvoiceNumberService.validate_template("{SEQMONTH}-{MM}-{YY}")
    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("{SEQMONTH}-{MM}")
        InvoiceNumberService.validate_template("{SEQMONTH}-{YY}")

    # month+company
    InvoiceNumberService.validate_template("{SEQMONTHANA}-{MM}-{YY}-{ANA}")
    with pytest.raises(ValueError):
        InvoiceNumberService.validate_template("{SEQMONTH}-{MM}-{YY}")
        InvoiceNumberService.validate_template("{SEQMONTH}-{MM}-{ANA}")


def test_invoice_number_service_generation(
    get_csrf_request_with_db, invoice_20170707, invoice_20170808
):
    tpl = "FC-{YYYY}{MM}-{SEQGLOBAL}"
    r = get_csrf_request_with_db()
    InvoiceNumberService.assign_number(r, invoice_20170707, tpl)
    InvoiceNumberService.assign_number(r, invoice_20170808, tpl)
    assert invoice_20170707.official_number == "FC-201707-1"
    assert invoice_20170808.official_number == "FC-201707-2"

    # Will not re-assign
    with pytest.raises(ValueError):
        InvoiceNumberService.assign_number(r, invoice_20170707, tpl)


def test_invoice_number_collision_avoidance_fix_1872(
    invoice_20170707,
    invoice_2018,
    get_csrf_request_with_db,
):
    # If the invoice sequence number hasn't been changed after switching to the
    # 4.2 version, we won't want it to provoque conflicts
    # It should disable uniqueness

    # goes back to zero and conflicts with other years invoices
    # but that was how enDI was configured by default before 4.2
    tpl = "{SEQYEAR}"
    r = get_csrf_request_with_db()
    # They will get the same official_number
    InvoiceNumberService.assign_number(r, invoice_20170707, tpl)

    # We ensure it doesn't raise (since the tpl doesn't ensure uniqueness)
    InvoiceNumberService.assign_number(r, invoice_2018, tpl)


# On a sortit le check de numéro de version de la transaction pour limiter l'impact de transaction superposée
# Dans le contexte des tests, ceci ne peut pas marcher
@pytest.mark.xfail
def test_invoice_number_collision_avoidance(
    invoice_20170707, invoice_2018, dbsession, get_csrf_request_with_db
):
    # With a template ensuring uniqueness, we should have an error
    tpl = "{YYYY}_{SEQYEAR}"

    # Since we set the number directly, no sequence index is filled
    # The next call to assign_number will use the same index and both invoices
    # will get the same number supposed to be unique
    invoice_20170707.official_number = tpl.format(
        YYYY=invoice_2018.date.year,
        SEQYEAR=1,
    )
    r = get_csrf_request_with_db()

    with pytest.raises(RetryableException):
        InvoiceNumberService.assign_number(r, invoice_2018, tpl)

    # With legacy tag, we want to allow that historic conflicts.
    invoice_20170707.legacy_number = True
    dbsession.merge(invoice_20170707)

    # Just check it raises nothing
    InvoiceNumberService.assign_number(r, invoice_2018, tpl)


def test_delete_invoice_with_sequence_number(
    invoice, dbsession, get_csrf_request_with_db
):
    r = get_csrf_request_with_db()
    InvoiceNumberService.assign_number(r, invoice, "{SEQGLOBAL}")
    dbsession.delete(invoice)
    dbsession.flush()
