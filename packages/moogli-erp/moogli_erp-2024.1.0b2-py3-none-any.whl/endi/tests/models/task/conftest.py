import pytest

from endi.models.sequence_number import (
    GlobalSequence,
    MonthCompanySequence,
    MonthSequence,
    SequenceNumber,
    YearSequence,
)


@pytest.fixture
def global_invoice_sequence(dbsession):
    from endi.models.task.task import Task

    return GlobalSequence(
        db_key=SequenceNumber.SEQUENCE_INVOICE_GLOBAL,
        init_value_config_key="global_invoice_sequence_init_value",
        types=["invoice", "cancelinvoice"],
        model_class=Task,
    )


@pytest.fixture
def year_invoice_sequence(dbsession):
    from endi.models.task.task import Task

    return YearSequence(
        db_key=SequenceNumber.SEQUENCE_INVOICE_YEAR,
        init_value_config_key="year_invoice_sequence_init_value",
        init_date_config_key="year_invoice_sequence_init_date",
        types=["invoice", "cancelinvoice"],
        model_class=Task,
    )


@pytest.fixture
def month_invoice_sequence(dbsession):
    from endi.models.task.task import Task

    return MonthSequence(
        db_key=SequenceNumber.SEQUENCE_INVOICE_MONTH,
        init_value_config_key="month_invoice_sequence_init_value",
        init_date_config_key="month_invoice_sequence_init_date",
        types=["invoice", "cancelinvoice"],
        model_class=Task,
    )


@pytest.fixture
def month_company_invoice_sequence(dbsession):
    from endi.models.task.task import Task

    return MonthCompanySequence(
        db_key=SequenceNumber.SEQUENCE_INVOICE_MONTH_COMPANY,
        company_init_date_fieldname="month_company_invoice_sequence_init_date",
        company_init_value_fieldname="month_company_invoice_sequence_init_value",
        types=["invoice", "cancelinvoice"],
        model_class=Task,
    )
