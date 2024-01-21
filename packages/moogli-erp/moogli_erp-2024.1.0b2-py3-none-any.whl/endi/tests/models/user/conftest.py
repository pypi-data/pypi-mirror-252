import datetime
import pytest


@pytest.fixture
def full_career_path_1(dbsession):
    from endi.models.career_path import CareerPath

    carreer_path = [
        CareerPath(start_date=datetime.date(2022, 12, 1), stage_type=None),
        CareerPath(start_date=datetime.date(2022, 12, 25), stage_type="entry"),
        CareerPath(start_date=datetime.date(2023, 2, 1), stage_type=None),
        CareerPath(start_date=datetime.date(2023, 3, 15), stage_type="contract"),
        CareerPath(start_date=datetime.date(2023, 6, 15), stage_type="amendment"),
        CareerPath(start_date=datetime.date(2023, 8, 15), stage_type="amendment"),
    ]
    for cp in carreer_path:
        dbsession.add(cp)
    dbsession.flush()
    return carreer_path


@pytest.fixture
def full_career_path_2(dbsession):
    from endi.models.career_path import CareerPath

    carreer_path = [
        CareerPath(start_date=datetime.date(2023, 4, 1), stage_type=None),
        CareerPath(start_date=datetime.date(2023, 5, 1), stage_type="entry"),
        CareerPath(start_date=datetime.date(2023, 9, 1), stage_type="exit"),
        CareerPath(start_date=datetime.date(2023, 9, 10), stage_type=None),
    ]
    for cp in carreer_path:
        dbsession.add(cp)
    dbsession.flush()
    return carreer_path


@pytest.fixture
def userdatas_with_full_career_path_1(
    dbsession,
    user,
    cae_situation_option,
    company,
    company2,
    full_career_path_1,
    social_status_option1,
    social_status_option2,
):
    from endi.models.user.userdatas import (
        UserDatas,
        UserDatasCustomFields,
        SocialStatusDatas,
    )

    user.companies = [company, company2]

    result = UserDatas(
        situation_situation=cae_situation_option,
        coordonnees_lastname="LASTNAME 1",
        coordonnees_firstname="Firstname 1",
        coordonnees_email1="userdatas1@test.fr",
        user_id=user.id,
        career_paths=full_career_path_1,
        coordonnees_family_status="isolated",
    )
    result.situation_situation_id = cae_situation_option.id

    ssd = SocialStatusDatas(
        step="entry", userdatas_id=result.id, social_status_id=social_status_option1.id
    )
    result.social_statuses = [ssd]
    ssd = SocialStatusDatas(
        step="today", userdatas_id=result.id, social_status_id=social_status_option1.id
    )
    ssd2 = SocialStatusDatas(
        step="today", userdatas_id=result.id, social_status_id=social_status_option2.id
    )
    result.today_social_statuses = [ssd, ssd2]

    cf = UserDatasCustomFields(id=result.id)
    result.custom_fields = cf
    result.custom_fields.exp__competences = "Origami"

    dbsession.add(result)
    dbsession.flush()
    user.userdatas = result
    return result


@pytest.fixture
def userdatas_with_full_career_path_2(
    dbsession, user2, cae_situation_option, full_career_path_2
):
    from endi.models.user.userdatas import UserDatas

    result = UserDatas(
        situation_situation=cae_situation_option,
        coordonnees_lastname="LASTNAME 2",
        coordonnees_firstname="Firstname 2",
        coordonnees_email1="userdatas2@test.fr",
        user_id=user2.id,
        career_paths=full_career_path_2,
    )
    result.situation_situation_id = cae_situation_option.id
    dbsession.add(result)
    dbsession.flush()
    user2.userdatas = result
    return result
