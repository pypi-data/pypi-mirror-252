def test_authentification_check_view(get_csrf_request_with_db):
    req = get_csrf_request_with_db()
    from endi.views.accounting.rest_api import authentification_check_view

    res = authentification_check_view(None, req)

    assert res["status"] == "success"


def test_operation_post(config, get_csrf_request_with_db, company, synchronized_upload):
    from endi.views.accounting.rest_api import (
        AccountingOperationRestView,
    )

    params = {
        "datas": [
            {
                "analytical_account": "0USER",
                "general_account": "GENERAL",
                "date": "2017-01-01",
                "label": "LABEL",
                "debit": "15",
                "credit": "15",
                "balance": "25",
            },
            {
                "analytical_account": "0USER",
                "general_account": "GENERAL",
                "date": "2018-01-01",
                "label": "LABEL",
                "debit": "15",
                "credit": "15",
                "balance": "25",
            },
            {
                "analytical_account": "0USER",
                "general_account": "GENERAL",
                "date": "2017-01-01",
                "label": "LABEL",
                "debit": "15",
                "credit": "15",
                "balance": "25",
            },
        ]
    }
    request = get_csrf_request_with_db(post=params)
    view = AccountingOperationRestView(request)
    result = view.bulk_post()

    first = result[0]

    assert first.analytical_account == "0USER"
    assert first.general_account == "GENERAL"
    assert first.debit == 15
    assert first.credit == 15
    assert first.balance == 25
    assert first.company_id == company.id

    # 2017
    assert first.upload_id == synchronized_upload.id

    # 2018
    assert result[1].upload_id != synchronized_upload.id

    # 2017
    assert result[2].upload_id == synchronized_upload.id


def test_solve_encoding_integration(dbsession, get_raw_request):
    from endi.views.accounting.rest_api import (
        AccountingOperationRestView,
    )

    params = '{"datas":[{"analytical_account":"0USER","general_account":"GENERAL","date":"2017-01-01","label":"\xe0cho","debit": "15","credit": "15","balance": "25"}]}'  # noqa : E251
    request = get_raw_request(request_body=params.encode("utf-8"))

    view = AccountingOperationRestView(request)
    result = view.bulk_post()

    assert len(result) == 1

    first = result[0]
    assert first.label == "àcho"
