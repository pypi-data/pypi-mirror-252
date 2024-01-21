from datetime import date
from freezegun import freeze_time
import pytest

from endi.models.user.userdatas import (
    UserDatas,
    CompanyDatas,
    CaeSituationOption,
)


def get_userdatas(option):
    result = UserDatas(
        situation_situation=option,
        coordonnees_lastname="test",
        coordonnees_firstname="test",
        coordonnees_email1="test@test.fr",
        activity_companydatas=[
            CompanyDatas(
                title="test enseigne",
                name="test enseigne",
            )
        ],
    )
    result.situation_situation_id = option.id
    return result


@pytest.fixture
def integre_cae_situation_option(dbsession):
    option = CaeSituationOption(label="Integre", is_integration=True)
    dbsession.add(option)
    dbsession.flush()
    return option


def test_gen_company(dbsession, userdatas):
    companies = userdatas.gen_companies()
    company = companies[0]
    assert company.id is None
    dbsession.add(company)
    dbsession.flush()


def test_company_existing(dbsession, userdatas, cae_situation_option):
    companies = userdatas.gen_companies()
    company = companies[0]
    assert company.id is None
    dbsession.add(company)
    dbsession.flush()

    userdatas2 = get_userdatas(cae_situation_option)
    dbsession.add(userdatas2)
    dbsession.flush()
    companies = userdatas2.gen_companies()
    company2 = companies[0]
    assert company2.id == company.id


@freeze_time("2019-01-02")
def test_age(userdatas):
    import datetime

    today = datetime.date.today()

    birthday = today.replace(year=today.year - 55)
    userdatas.coordonnees_birthday = birthday
    assert userdatas.age == 55

    birthday = today.replace(year=today.year + 1)
    userdatas.coordonnees_birthday = birthday
    assert userdatas.age == -1


@pytest.mark.xfail
def test_salary_compute(dbsession, userdatas):
    userdatas.parcours_taux_horaire = 5
    userdatas.parcours_num_hours = 35
    dbsession.merge(userdatas)
    dbsession.flush()
    assert userdatas.parcours_salary == 175
    userdatas.parcours_taux_horaire = 5
    userdatas.parcours_num_hours = None
    dbsession.merge(userdatas)
    dbsession.flush()
    assert userdatas.parcours_salary == 0


@pytest.mark.xfail
def test_add_situation_change_handler(
    dbsession, userdatas, integre_cae_situation_option
):
    import datetime

    assert len(userdatas.situation_history) == 1
    userdatas.situation_situation_id = integre_cae_situation_option.id
    dbsession.merge(userdatas)
    dbsession.flush()
    today = datetime.date.today()
    assert len(userdatas.situation_history) == 2
    assert (
        userdatas.situation_history[-1].situation_id == integre_cae_situation_option.id
    )
    assert userdatas.situation_history[-1].date == today


def test_userdatas_utils(
    userdatas_with_full_career_path_1, userdatas_with_full_career_path_2, mk_config
):
    from endi.models.user.userdatas import STATUS_OPTIONS
    from endi.models.user.utils import (
        get_userdatas_first_step,
        get_userdatas_last_step,
        get_userdatas_steps_on_period,
        get_userdatas_entry_date,
        get_userdatas_exit_date,
        get_userdatas_exit,
        is_userdatas_active_on_period,
        get_all_userdatas_active_on_period,
        get_user_analytical_accounts,
        get_tuple_option_label,
        get_social_statuses_label,
        get_active_custom_fields,
        get_active_custom_fields_labels,
        get_custom_field_value_string,
    )

    date1 = date(2023, 1, 1)
    date2 = date(2023, 3, 31)
    date3 = date(2023, 10, 1)
    date4 = date(2023, 12, 31)
    u1 = userdatas_with_full_career_path_1
    u2 = userdatas_with_full_career_path_2
    uid1 = u1.id
    uid2 = u2.id

    assert get_userdatas_first_step(uid1).start_date == date(2022, 12, 25)
    assert get_userdatas_first_step(uid1, date1).start_date == date(2023, 3, 15)
    assert get_userdatas_first_step(uid1, None, ["amendment"]).start_date == date(
        2023, 6, 15
    )

    assert get_userdatas_last_step(uid1).start_date == date(2023, 8, 15)
    assert get_userdatas_last_step(uid2).start_date == date(2023, 9, 1)
    assert get_userdatas_last_step(uid1, date1).start_date == date(2022, 12, 25)
    assert get_userdatas_last_step(uid2, date1) == None
    assert get_userdatas_last_step(uid1, None, ["contract"]).start_date == date(
        2023, 3, 15
    )

    assert len(get_userdatas_steps_on_period(uid1, date1, date2)) == 1
    assert len(get_userdatas_steps_on_period(uid1, date1, date4)) == 3
    assert len(get_userdatas_steps_on_period(uid1, date1, date4, ["amendment"])) == 2
    assert len(get_userdatas_steps_on_period(uid2, date1, date2)) == 0
    assert len(get_userdatas_steps_on_period(uid2, date1, date4)) == 2
    assert len(get_userdatas_steps_on_period(uid2, date1, date4, ["amendment"])) == 0

    assert get_userdatas_entry_date(uid1) == date(2022, 12, 25)
    assert get_userdatas_entry_date(uid2) == date(2023, 5, 1)

    assert get_userdatas_exit_date(uid1) == None
    assert get_userdatas_exit_date(uid2) == date(2023, 9, 1)

    assert get_userdatas_exit(uid1) == None
    assert get_userdatas_exit(uid2).start_date == date(2023, 9, 1)

    assert is_userdatas_active_on_period(uid1, date1, date2) == True
    assert is_userdatas_active_on_period(uid1, date2, date3) == True
    assert is_userdatas_active_on_period(uid1, date3, date4) == True
    assert is_userdatas_active_on_period(uid2, date1, date2) == False
    assert is_userdatas_active_on_period(uid2, date2, date3) == True
    assert is_userdatas_active_on_period(uid2, date3, date4) == False

    assert len(get_all_userdatas_active_on_period(date1, date2)) == 1
    assert len(get_all_userdatas_active_on_period(date2, date3)) == 2
    assert len(get_all_userdatas_active_on_period(date3, date4)) == 1
    assert len(get_all_userdatas_active_on_period(date1, date4)) == 2
    assert get_all_userdatas_active_on_period(date1, date4)[0].id == uid1

    assert get_user_analytical_accounts(u1.user.id) == "0USER, 1USER"

    assert (
        get_tuple_option_label(STATUS_OPTIONS, u1.coordonnees_family_status)
        == "Séparé(e)"
    )

    assert get_social_statuses_label(u1.social_statuses) == "Social status 1"
    assert (
        get_social_statuses_label(u1.today_social_statuses)
        == "Social status 1 ; Social status 2"
    )

    mk_config("userdatas_active_custom_fields", '["exp__diplome", "exp__competences"]')
    assert len(get_active_custom_fields()) == 2
    assert "exp__competences" in get_active_custom_fields()
    assert "Compétences" in get_active_custom_fields_labels()
    assert get_custom_field_value_string(u1, "exp__competences") == "Origami"
