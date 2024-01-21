"""
    test treasury files views
"""
import os
import pytest
from unittest.mock import Mock
from pyramid.exceptions import HTTPForbidden, HTTPNotFound
from endi.views.treasury_files import (
    TreasuryFilesView,
    IncomeStatementFilesView,
    SalarySheetFilesView,
    isprefixed,
    get_code_compta,
    code_is_not_null,
    digit_subdirs,
    file_display,
    list_files,
    AdminTreasuryView,
    MailTreasuryFilesView,
    get_root_directory,
)

CODE = "125"


@pytest.fixture
def company_125(dbsession):
    from endi.models.company import Company

    c = Company(name="testit", code_compta=CODE, email="a@a.fr")
    dbsession.add(c)
    return c


def test_digit_subdirs(settings):
    path = os.path.join(settings["endi.ftpdir"], "tresorerie", "2010")
    dirs = list(digit_subdirs(path))
    assert len(dirs) == 12


def test_list_files(settings):
    path = os.path.join(settings["endi.ftpdir"], "tresorerie", "2010", "1")
    assert len(list_files(path, prefix="")) == 12
    assert len(list_files(path, prefix="12")) == 0
    assert len(list_files(path, prefix=CODE + "6")) == 0
    assert len(list_files(path, prefix=CODE)) == 4


def test_list_files_sorted(settings):
    path = os.path.join(settings["endi.ftpdir"], "tresorerie", "2010", "1")
    files = list_files(path, prefix=CODE)
    prev = files[0]
    for f_ in files[1:]:
        assert f_.name > prev.name
        prev = f_


def test_isprefixed():
    assert isprefixed("256_bar.pdf", "256")
    assert isprefixed("256_bar.pdf")
    assert not isprefixed("256_bar.pdf", "32")
    assert not isprefixed("256_bar.pdf", "2567")
    assert not isprefixed("256_bar.pdf", "25")


def test_get_code_compta():
    with pytest.raises(Exception):
        get_code_compta("0")


def test_code_is_not_null():
    assert code_is_not_null("2")
    for i in "0", "", None:
        assert not code_is_not_null(i)


def test_view(config, get_csrf_request_with_db):
    request = get_csrf_request_with_db()
    request.context = Mock(code_compta=CODE)
    config.add_route("treasury_files", "/")
    for factory in IncomeStatementFilesView, SalarySheetFilesView, TreasuryFilesView:
        view = factory(request)
        result = view.__call__()
        assert len(list(result["documents"].keys())) == 2
        assert len(result["documents"]["2010"]) == 12


def test_nutt(config, get_csrf_request_with_db):
    request = get_csrf_request_with_db()
    request.context = Mock(code_compta="")
    config.add_route("treasury_files", "/")
    for factory in IncomeStatementFilesView, SalarySheetFilesView, TreasuryFilesView:
        view = factory(request)
        assert view()["documents"] == {}


def test_file_view(get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={"name": "/resultat/2011/1/125_1_test.pdf"})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert result.content_disposition == "attachment; filename=125_1_test.pdf"
    assert result.content_type == "application/pdf"


def test_forbidden_nocode(get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={"name": "/resultat/2011/1/125_test.pdf"})
    request.context = Mock(code_compta="")
    result = file_display(request)
    assert isinstance(result, HTTPForbidden)


def test_forbidden_wrond_code(get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={"name": "/resultat/2011/1/125_test.pdf"})
    request.context = Mock(code_compta=CODE + "1")
    result = file_display(request)
    assert isinstance(result, HTTPForbidden)


def test_forbidden_notsubdir(get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={"name": "../../test/125_test.pdf"})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert isinstance(result, HTTPForbidden)


def test_notfound(get_csrf_request_with_db):
    request = get_csrf_request_with_db(post={"name": "/resultat/2011/1/125_test2.pdf"})
    request.context = Mock(code_compta=CODE)
    result = file_display(request)
    assert isinstance(result, HTTPNotFound)


def test_admin_treasury(config, get_csrf_request_with_db, company_125):
    config.add_route(
        "admin_treasury_files",
        "/{filetype}/{year}/{month}/",
    )
    view = AdminTreasuryView(None, get_csrf_request_with_db())
    result_dict = view()
    assert set(result_dict["datas"].keys()) == set(("2010", "2011"))
    assert result_dict["datas"]["2011"]["9"]["nbfiles"] == 4


def test_mail_treasury_files(dbsession, config, get_csrf_request_with_db, company_125):
    request = get_csrf_request_with_db()
    request.matchdict = {"filetype": "salaire", "year": "2010", "month": "1"}
    view = MailTreasuryFilesView(None, request)
    result_dict = view()
    datas = result_dict["datas"]
    assert len(list(datas.keys())) == 1
    for file_ in list(datas.values())[0]:
        assert file_["file"].code == file_["company"].code_compta

    form_datas = {
        "force": False,
        "mails": [
            {"company_id": company_125.id, "attachment": "125_1_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_2_test.pdf"},
        ],
        "mail_subject": "Sujet",
        "mail_message": "Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(
        datas, form_datas, get_root_directory(request), "2010", "1"
    )
    assert len(mails) == 2
    assert mails[0]["message"] == "Message a@a.fr 2010 1"
    assert mails[0]["email"] == "a@a.fr"

    sent_file = datas[company_125.id][0]["file"]
    from endi_celery.models import store_sent_mail

    history = store_sent_mail(sent_file.path, sent_file.datas, company_125.id)
    dbsession.add(history)

    # Not force and already in history
    form_datas = {
        "force": False,
        "mails": [
            {"company_id": company_125.id, "attachment": "125_0_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_1_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_2_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_3_test.pdf"},
        ],
        "mail_subject": "Sujet",
        "mail_message": "Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(
        datas, form_datas, get_root_directory(request), "2010", "1"
    )
    assert len(mails) == 3

    # Force and already in history
    form_datas = {
        "force": True,
        "mails": [
            {"company_id": company_125.id, "attachment": "125_0_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_1_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_2_test.pdf"},
            {"company_id": company_125.id, "attachment": "125_3_test.pdf"},
        ],
        "mail_subject": "Sujet",
        "mail_message": "Message {company.email} {year} {month}",
    }

    mails = view._prepare_mails(
        datas, form_datas, get_root_directory(request), "2010", "1"
    )
    assert len(mails) == 4

    # Invalid submitted datas
    form_datas = {
        "force": True,
        "mails": [
            {"company_id": -15, "attachment": "125_3_test.pdf"},
        ],
        "mail_subject": "Sujet",
        "mail_message": "Message {company.email} {year} {month}",
    }

    with pytest.raises(Exception):
        mails = view._prepare_mails(
            datas, form_datas, get_root_directory(request), "2010", "1"
        )
