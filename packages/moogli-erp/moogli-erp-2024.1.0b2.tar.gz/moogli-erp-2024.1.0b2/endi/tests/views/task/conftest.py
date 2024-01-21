import pytest


@pytest.fixture
def pdf_config(dbsession, config):
    from endi.models.config import Config

    Config.set("coop_cgv", "Conditions générales de vente")
    Config.set("coop_pdffootertitle", "Pied de page")
    Config.set("coop_pdffootertext", "Contenu du pied de page")
    Config.set("coop_pdffootercourse", "Formation professionnelle")
    Config.set("sale_pdf_filename_template", "{type_document}_{numero}")
    dbsession.flush()

    config.include("endi.panels.task")


@pytest.fixture
def task_line(mk_task_line, tva, product):
    # TTC = 120 €
    return mk_task_line(cost=10000000, tva=tva.value, product=product)


@pytest.fixture
def full_estimation(
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
    estimation.line_groups = [task_line_group]
    estimation.discounts = [discount_line]
    estimation.payment_lines = [payment_line, payment_line2]
    estimation.workplace = "workplace"
    estimation.mentions = [mention]
    estimation.expenses_ht = 1000000
    estimation.validity_duration = "3 mois"
    estimation.start_date = date_20190101
    estimation = dbsession.merge(estimation)
    estimation.manualDeliverables = 1
    dbsession.flush()
    return estimation


@pytest.fixture
def business(dbsession, full_estimation, mk_business, default_business_type):
    business = mk_business(name=full_estimation.name)
    business.estimations = [full_estimation]
    full_estimation.business_type_id = default_business_type.id
    full_estimation.businesses = [business]
    dbsession.merge(full_estimation)
    dbsession.merge(business)
    dbsession.flush()
    return business
