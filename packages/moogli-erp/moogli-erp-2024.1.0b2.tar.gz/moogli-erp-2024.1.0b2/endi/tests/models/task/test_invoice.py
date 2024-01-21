import datetime


def test_set_numbers(invoice, cancelinvoice):
    invoice.date = datetime.date(2012, 12, 1)
    invoice.set_numbers(15, 1)
    assert invoice.internal_number == "Company 2012-12 F15"
    assert invoice.name == "Facture 1"

    cancelinvoice.date = datetime.date(2012, 12, 1)
    cancelinvoice.set_numbers(15, 5)
    assert cancelinvoice.name == "Avoir 5"
    assert cancelinvoice.internal_number == "Company 2012-12 A15"


def test_set_deposit_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_deposit_label()
    assert invoice.name == "Facture d'acompte 8"


def test_set_sold_label(invoice):
    invoice.set_numbers(5, 8)
    invoice.set_sold_label()
    assert invoice.name == "Facture de solde 8"


def test_valid_invoice(config, dbsession, invoice, get_csrf_request_with_db, user):
    req = get_csrf_request_with_db(user=user)
    dbsession.add(invoice)
    dbsession.flush()
    config.testing_securitypolicy(userid="test", identity=user, permissive=True)

    invoice.set_status("wait", req)
    dbsession.merge(invoice)
    dbsession.flush()
    invoice.set_status("valid", req)
    assert invoice.official_number == "1"


def test_gen_cancelinvoice(get_csrf_request_with_db, dbsession, full_invoice, user):
    # test using a different financial year between invoice and cancel invoice
    full_invoice.financial_year = 2019

    cinv = full_invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    dbsession.add(cinv)
    dbsession.flush()

    assert cinv.total_ht() == -1 * full_invoice.total_ht()
    today = datetime.date.today()

    assert cinv.date == today

    # cancel invoice date should be the current year rather than
    # invoice's financial year (issue #3161)
    assert cinv.financial_year == today.year

    assert cinv.mentions == full_invoice.mentions
    assert cinv.address == full_invoice.address
    assert cinv.workplace == full_invoice.workplace
    assert cinv.project == full_invoice.project
    assert cinv.company == full_invoice.company
    assert cinv.phase == full_invoice.phase
    assert cinv.start_date == full_invoice.start_date


def test_gen_cancelinvoice_mode_ttc(get_csrf_request_with_db, dbsession, invoice, user):
    invoice.mode = "ttc"
    cinv = invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    dbsession.add(cinv)
    dbsession.flush()
    assert cinv.mode == invoice.mode
    assert cinv.mode == "ttc"  # to be sure


def test_gen_cancelinvoice_mode_ht(get_csrf_request_with_db, dbsession, invoice, user):
    cinv = invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    dbsession.add(cinv)
    dbsession.flush()
    assert cinv.mode == invoice.mode
    assert cinv.mode == "ht"  # default value


def test_gen_cancelinvoice_mode_ttc_bug_3680(
    get_csrf_request_with_db, dbsession, invoice, user, mk_discount_line
):
    invoice.mode = "ttc"
    invoice.discounts = [mk_discount_line(amount=10000000)]
    dbsession.merge(invoice)
    dbsession.flush()
    cinv = invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    assert cinv.all_lines[-1].mode == "ttc"
    assert cinv.all_lines[-1].cost == 10000000


def test_gen_cancelinvoice_decimal_to_display(
    get_csrf_request_with_db, dbsession, invoice, user, company
):
    company.decimal_to_display = 5  # default was 2
    cinv = invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    assert cinv.decimal_to_display == 2  # Should not be affected by the change


def test_gen_cancelinvoice_with_payment(
    get_csrf_request_with_db, dbsession, full_invoice, tva, mode, mk_payment, user
):
    payment = mk_payment(amount=10000000)
    full_invoice.payments = [payment]
    cinv = full_invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    assert (
        len(cinv.default_line_group.lines)
        == len(full_invoice.default_line_group.lines) + len(full_invoice.discounts) + 1
    )

    # Le paiement est indiqué ttc, ici on a le HT (tva inversée)
    assert cinv.default_line_group.lines[-1].cost == 8333333
    assert cinv.default_line_group.lines[-1].tva == 2000


def test_invoice_topay(full_invoice, mk_payment, user):
    full_invoice.payments = [mk_payment(amount=2000000)]

    assert full_invoice.paid() == 2000000
    assert full_invoice.topay() == full_invoice.total() - 2000000


def test_check_resulted(full_invoice, mk_payment, user):
    full_invoice.payments = [mk_payment(amount=int(full_invoice.topay()))]

    full_invoice.status = "valid"
    full_invoice.paid_status = "paid"
    full_invoice.check_resulted()
    assert full_invoice.paid_status == "resulted"


def test_check_resulted_force(full_invoice, request_with_config, user):
    full_invoice.status = "valid"
    full_invoice.paid_status = "paid"
    full_invoice.check_resulted(force_resulted=True)
    assert full_invoice.paid_status == "resulted"


def test_resulted_auto_more(
    full_invoice,
    mk_payment,
    request_with_config,
    user,
):
    # the payment is more than ttc
    full_invoice.payments = [mk_payment(amount=int(full_invoice.topay()))]

    full_invoice.status = "valid"
    full_invoice.paid_status = "paid"
    full_invoice.check_resulted()
    assert full_invoice.paid_status == "resulted"


def test_historize_paid_status(
    full_invoice,
    mk_payment,
    request_with_config,
    user,
):
    full_invoice.payments = [mk_payment(amount=full_invoice.topay())]

    full_invoice.status = "valid"
    full_invoice.paid_status = "paid"
    full_invoice.check_resulted()
    full_invoice.historize_paid_status(user)
    assert full_invoice.statuses[-1].status == "resulted"
    assert full_invoice.statuses[-1].user_id == user.id


def test_payment_get_amount(mk_payment):
    payment = mk_payment(amount=1895000)
    assert payment.get_amount() == 1895000


def test_set_default_display_units(mk_invoice, dbsession, user):
    # Le plugin sap ajoute des automatismes sur des évènements SQLAlchemy
    # On doit les désactiver ici
    from endi.plugins.sap.models.task.tasks import (
        stop_listening,
        start_listening,
        is_listening,
    )

    sap_active = is_listening()
    if sap_active:
        stop_listening()
    from endi.models.config import Config

    Config.set("task_display_units_default", "1")

    invoice1 = mk_invoice()
    invoice1.set_display_units()
    assert invoice1.display_units == "1"

    mk_invoice(display_units="0", status="valid")

    invoice3 = mk_invoice()
    invoice3.set_display_units()
    assert invoice3.status == "draft"
    assert invoice3.display_units == 0
    if sap_active:
        start_listening()


def test_set_default_display_ttc(mk_invoice, dbsession, user):
    # Le plugin sap ajoute des automatismes sur des évènements SQLAlchemy
    # On doit les désactiver ici
    from endi.plugins.sap.models.task.tasks import (
        stop_listening,
        start_listening,
        is_listening,
    )

    sap_active = is_listening()
    if sap_active:
        stop_listening()
    from endi.models.config import Config

    Config.set("task_display_ttc_default", "1")

    invoice1 = mk_invoice()
    invoice1.set_display_ttc()
    assert invoice1.display_ttc == "1"

    mk_invoice(display_ttc="0", status="valid")

    invoice3 = mk_invoice()
    invoice3.set_display_ttc()
    assert invoice3.status == "draft"
    assert invoice3.display_ttc == 0
    if sap_active:
        start_listening()
