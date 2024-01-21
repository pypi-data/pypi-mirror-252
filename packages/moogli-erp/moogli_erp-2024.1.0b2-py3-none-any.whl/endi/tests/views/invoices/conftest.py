import pytest


@pytest.fixture
def full_cancelinvoice(
    dbsession,
    mk_cancelinvoice,
    full_invoice,
    task_line_group,
    task_line,
    user,
    mention,
    date_20190101,
    mk_task_line_group,
    mk_task_line,
):
    cancelinvoice = mk_cancelinvoice()
    # TTC  : -1 * (120 - 12  + 12 €)
    cancelinvoice.invoice_id = full_invoice.id
    group = cancelinvoice.line_groups[0]
    mk_task_line(
        cost=-1 * full_invoice.total_ht(),
        group=group,
        tva=full_invoice.all_lines[0].tva,
    )
    cancelinvoice.workplace = "workplace"
    cancelinvoice.mentions = [mention]

    cancelinvoice.payment_conditions = "Test"
    cancelinvoice.description = "Description"
    cancelinvoice.start_date = date_20190101
    cancelinvoice = dbsession.merge(cancelinvoice)
    dbsession.flush()
    return cancelinvoice
