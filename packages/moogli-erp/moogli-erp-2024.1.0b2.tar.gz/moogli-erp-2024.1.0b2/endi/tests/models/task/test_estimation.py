import datetime


def test_estimation_set_numbers(full_estimation):
    full_estimation.date = datetime.date(1969, 7, 1)
    full_estimation.set_numbers(5, 18)
    assert full_estimation.internal_number == "Company 1969-07 D5"
    assert full_estimation.name == "Devis 18"
    assert full_estimation.project_index == 18


def test_duplicate_payment_line(payment_line):
    newline = payment_line.duplicate()
    for i in ("order", "description", "amount"):
        assert getattr(newline, i) == getattr(payment_line, i)

    today = datetime.date.today()
    assert newline.date == today


def test_set_default_validity_duration(mk_estimation):
    # https://framagit.org/endi/endi/-/issues/2181
    from endi.models.config import Config

    Config.set("estimation_validity_duration_default", "AAA")

    estimation1 = mk_estimation()
    estimation1.set_default_validity_duration()
    assert estimation1.validity_duration == "AAA"

    mk_estimation(validity_duration="BBB")

    estimation3 = mk_estimation()
    estimation3.set_default_validity_duration()
    assert estimation3.validity_duration == "BBB"


def test_set_default_display_units(mk_estimation, dbsession, user):
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

    estimation1 = mk_estimation()
    estimation1.set_display_units()
    assert estimation1.display_units == "1"

    mk_estimation(display_units=0, status="valid")

    estimation3 = mk_estimation()
    estimation3.set_display_units()
    assert estimation3.status == "draft"
    assert estimation3.display_units == 0
    if sap_active:
        start_listening()


def test_set_default_display_ttc(mk_estimation, dbsession, user):
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

    estimation1 = mk_estimation()
    estimation1.set_display_ttc()
    assert estimation1.display_ttc == "1"

    mk_estimation(display_ttc=0, status="valid")

    estimation3 = mk_estimation()
    estimation3.set_display_ttc()
    assert estimation3.status == "draft"
    assert estimation3.display_ttc == 0
    if sap_active:
        start_listening()
