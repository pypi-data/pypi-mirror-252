def test_create_update_urssaf_payment_request(urssaf_payment_request, dbsession):

    upr = urssaf_payment_request
    assert upr.update_from_urssaf_status_code("20") == True
    dbsession.merge(upr)

    assert upr.request_comment == (
        "Le client a été prévenu qu'il doit valider ou rejeter"
        " la demande de paiement."
    )
    assert upr.urssaf_status_code == "20"
    assert upr.request_status == "waiting"

    assert upr.update_from_urssaf_status_code("20") == False


def test_request_status_title(urssaf_payment_request):
    assert urssaf_payment_request.urssaf_status_title == "Inconnu"

    urssaf_payment_request.urssaf_status_code = "20"
    assert urssaf_payment_request.urssaf_status_title == "En attente de validation"


def test_request_status_description(urssaf_payment_request):
    assert urssaf_payment_request.urssaf_status_description == ""

    urssaf_payment_request.urssaf_status_code = "50"
    assert (
        urssaf_payment_request.urssaf_status_description
        == "Le prélèvement de la demande de paiement est en cours."
    )


def test_request_status_invoice_relationship(urssaf_payment_request, invoice):
    assert urssaf_payment_request.invoice == invoice
    assert invoice.urssaf_payment_request == urssaf_payment_request
