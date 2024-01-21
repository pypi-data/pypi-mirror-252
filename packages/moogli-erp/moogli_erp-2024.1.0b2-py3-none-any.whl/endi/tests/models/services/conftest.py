import pytest


@pytest.fixture
def payment_line(mk_payment_line):
    return mk_payment_line(amount=15000000)


@pytest.fixture
def full_estimation(
    get_csrf_request_with_db,
    dbsession,
    estimation,
    task_line_group,
    task_line,
    user,
    mention,
    discount_line,
    payment_line,
    payment_line2,
    mk_task_line,
    mk_tva,
    mk_product,
    date_20190101,
):
    tva = mk_tva(name="7%", value=700, default=False)
    product = mk_product(name="product7", tva=tva)
    # TTC  : 100 + 20/100 * 100 + 100 + 7%*100 - 12  + 12 €
    # accompte : 10/100
    # payments : 1er paiement de 150 + solde
    task_line_group.lines = [
        task_line,
        mk_task_line(cost=10000000, tva=700, product=product),
    ]
    estimation.deposit = 10
    estimation.display_units = 1
    estimation.line_groups = [task_line_group]
    estimation.discounts = [discount_line]
    estimation.payment_lines = [payment_line, payment_line2]
    estimation.workplace = "workplace"
    estimation.mentions = [mention]
    estimation.expenses_ht = 1000000
    estimation = dbsession.merge(estimation)
    estimation.manualDeliverables = 1
    estimation.validity_duration = "3 mois"
    estimation.start_date = date_20190101
    dbsession.flush()
    estimation.cache_totals(get_csrf_request_with_db())

    return estimation


@pytest.fixture
def full_invoice(
    get_csrf_request_with_db,
    dbsession,
    invoice,
    task_line_group,
    task_line,
    user,
    mention,
    discount_line,
    date_20190101,
):
    # TTC  : 120 - 12  + 12 €
    task_line_group.lines = [task_line]
    invoice.line_groups = [task_line_group]
    invoice.discounts = [discount_line]
    invoice.workplace = "workplace"
    invoice.mentions = [mention]
    invoice.expenses_ht = 1000000
    invoice.start_date = date_20190101
    invoice = dbsession.merge(invoice)
    dbsession.flush()
    invoice.cache_totals(get_csrf_request_with_db())
    return invoice


@pytest.fixture
def business(dbsession, mk_business, full_estimation, default_business_type):
    business = mk_business()
    business.estimations = [full_estimation]
    dbsession.merge(business)
    full_estimation.business_type_id = default_business_type.id
    full_estimation.businesses = [business]
    dbsession.merge(full_estimation)
    dbsession.flush()
    return business


@pytest.fixture
def business_with_progress_invoicing(dbsession, business, full_estimation):
    from endi.models.project.services.business import BusinessService

    business.estimations[0].status = "valid"
    business.invoicing_mode = business.PROGRESS_MODE
    # On crée les statut de facturation à l'avancement
    BusinessService.populate_progress_invoicing_status(business)
    dbsession.merge(business.estimations[0])
    dbsession.merge(business)
    dbsession.flush()
    return business


@pytest.fixture
def progress_invoicing_invoice(
    get_csrf_request_with_db, dbsession, business_with_progress_invoicing, user
):
    from endi.models.project.services.business import BusinessService

    invoice = business_with_progress_invoicing.add_invoice(
        get_csrf_request_with_db(), user
    )

    # On construit la structure de données attendues pour la génération des
    # lignes de prestation
    appstruct = {}
    for status in business_with_progress_invoicing.progress_invoicing_group_statuses:
        appstruct[status.id] = {}
        for line_status in status.line_statuses:
            appstruct[status.id][line_status.id] = 10
    # On populate notre facture
    BusinessService.populate_progress_invoicing_lines(
        business_with_progress_invoicing,
        invoice,
        appstruct,
    )
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def expense_line_tva_on_margin(
    business,
    mk_expense_line,
    expense_type_tva_on_margin,
    expense_sheet,
):
    return mk_expense_line(
        expense_type=expense_type_tva_on_margin,
        ht=44,
        tva=4,
        business_id=business.id,
        project_id=business.project_id,
        sheet_id=expense_sheet.id,
    )  # 48 TTC


@pytest.fixture
def expense_line_no_tva_on_margin(
    business,
    mk_expense_line,
    expense_sheet,
):
    return mk_expense_line(
        ht=12,
        tva=2,
        business_id=business.id,
        project_id=business.project_id,
        sheet_id=expense_sheet.id,
    )  # 14 TTC
