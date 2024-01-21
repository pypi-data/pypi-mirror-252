import pytest
import io

csv_string = """Nom;Email 1;PRénom;Unknown;Status
Arthur;b.arthur;Bienaimé;Datas;CaeSituationOption
"""


def get_buffer():
    return io.StringIO(csv_string)


@pytest.fixture
def csv_datas():
    import csv

    f = csv.DictReader(
        get_buffer(),
        quotechar='"',
        delimiter=";",
    )
    return f


@pytest.fixture
def association_handler(wsgi_app):
    from endi_celery.tasks.csv_import import get_csv_import_associator

    return get_csv_import_associator("userdatas")


@pytest.fixture
def userdata(dbsession, cae_situation_option):
    from endi.models.user.userdatas import UserDatas

    u = UserDatas(
        situation_situation_id=cae_situation_option.id,
        coordonnees_firstname="firstname",
        coordonnees_lastname="lastname",
        coordonnees_email1="mail@mail.com",
    )
    dbsession.add(u)
    dbsession.flush()
    return u


def test_guess_association_dict(csv_datas, association_handler):
    res = association_handler.guess_association_dict(csv_datas.fieldnames)
    assert res["PRénom"] == "coordonnees_firstname"
    assert res["Nom"] == "coordonnees_lastname"
    assert res["Unknown"] is None

    res = association_handler.guess_association_dict(
        csv_datas.fieldnames, {"Nom": "coordonnees_ladiesname"}
    )
    assert res["PRénom"] == "coordonnees_firstname"
    assert res["Nom"] == "coordonnees_ladiesname"
    # Test field exclusion
    from endi_celery.tasks.csv_import import CsvImportAssociator
    from endi.models.user.userdatas import UserDatas

    associator = CsvImportAssociator(UserDatas, excludes=("coordonnees_lastname",))
    res = associator.guess_association_dict(
        csv_datas.fieldnames,
    )
    assert res["Nom"] == "name"


def test_collect_kwargs(association_handler):
    association_dict = {"a": "A match", "b": None}

    association_handler.set_association_dict(association_dict)

    line = {"a": "A data", "b": "B data", "c": "C data"}
    kwargs, trashed = association_handler.collect_args(line)

    assert kwargs == {"A match": "A data"}
    assert trashed == {"b": "B data", "c": "C data"}


def test_import_line(dbsession, csv_datas, association_handler, cae_situation_option):
    from endi_celery.tasks.csv_import import CsvImporter, DEFAULT_ID_LABEL
    from endi.models.user.userdatas import UserDatas

    association_dict = {
        "Status": "situation_situation",
        "PRénom": "coordonnees_firstname",
        "Nom": "coordonnees_lastname",
        "Email 1": "coordonnees_email1",
    }
    association_handler.set_association_dict(association_dict)

    line = next(csv_datas)
    importer = CsvImporter(
        dbsession,
        UserDatas,
        get_buffer(),
        association_handler,
        action="insert",
    )
    res, msg = importer.import_line(line.copy())

    assert res.coordonnees_firstname == "Bienaimé"
    assert res.coordonnees_lastname == "Arthur"
    assert res.situation_situation.label == "CaeSituationOption"
    assert sorted(importer.unhandled_datas[0].keys()) == sorted(
        [DEFAULT_ID_LABEL, "Unknown"]
    )
    assert importer.in_error_lines == []

    # We pop a mandatory argument
    association_dict.pop("Nom")
    association_handler.set_association_dict(association_dict)

    from endi_celery.exception import MissingMandatoryArgument

    with pytest.raises(MissingMandatoryArgument):
        importer = CsvImporter(
            dbsession,
            UserDatas,
            get_buffer(),
            association_handler,
            action="insert",
        )


def test_import_line_callback(
    dbsession, csv_datas, association_handler, cae_situation_option
):
    from endi_celery.tasks.csv_import import CsvImporter
    from endi_celery.tasks import _import_userdatas_add_related_user
    from endi.models.user.userdatas import UserDatas

    association_dict = {
        "Status": "situation_situation",
        "PRénom": "coordonnees_firstname",
        "Nom": "coordonnees_lastname",
        "Email 1": "coordonnees_email1",
    }
    association_handler.set_association_dict(association_dict)

    line = next(csv_datas)
    importer = CsvImporter(
        dbsession,
        UserDatas,
        get_buffer(),
        association_handler,
        action="insert",
        callbacks=[_import_userdatas_add_related_user],
    )
    res, msg = importer.import_line(line.copy())

    assert res.coordonnees_firstname == "Bienaimé"
    assert res.coordonnees_lastname == "Arthur"
    assert res.situation_situation.label == "CaeSituationOption"
    assert res.user.firstname == "Bienaimé"
    assert res.user.lastname == "Arthur"
    assert res.user.email == "b.arthur"


def test_update_line(association_handler, userdata, dbsession):
    from endi_celery.tasks.csv_import import CsvImporter
    from endi.models.user.userdatas import UserDatas

    association_dict = {
        "firstname": "coordonnees_firstname",
        "email": "coordonnees_email2",
    }
    association_handler.set_association_dict(association_dict)

    importer = CsvImporter(
        dbsession, UserDatas, get_buffer(), association_handler, action="update"
    )
    new_datas = {"id": str(userdata.id), "firstname": "Jane", "email": "g@p.fr"}
    res, msg = importer.import_line(new_datas)

    assert res.coordonnees_lastname == "lastname"
    assert res.coordonnees_firstname == "firstname"
    assert res.coordonnees_email2 == "g@p.fr"


def test_override_line(dbsession, association_handler, userdata):
    from endi_celery.tasks.csv_import import CsvImporter
    from endi.models.user.userdatas import UserDatas

    association_dict = {
        "firstname": "coordonnees_firstname",
        "email": "coordonnees_email2",
    }
    association_handler.set_association_dict(association_dict)

    importer = CsvImporter(
        dbsession, UserDatas, get_buffer(), association_handler, action="override"
    )
    new_datas = {"id": str(userdata.id), "firstname": "Jane", "email": "g@p.fr"}
    res, msg = importer.import_line(new_datas)

    assert res.coordonnees_lastname == "lastname"
    assert res.coordonnees_firstname == "Jane"
    assert res.coordonnees_email2 == "g@p.fr"


def test_identification_key(dbsession, association_handler, userdata):
    """
    Test if we use another key than "id" to identify the duplicate entries
    """
    from endi_celery.tasks.csv_import import CsvImporter
    from endi.models.user.userdatas import UserDatas

    association_dict = {
        "firstname": "coordonnees_firstname",
        "email": "coordonnees_email1",
        "test": "coordonnees_emergency_name",
    }
    association_handler.set_association_dict(association_dict)

    importer = CsvImporter(
        dbsession,
        UserDatas,
        get_buffer(),
        association_handler,
        action="update",
        id_key="coordonnees_email1",
    )
    # Ici on utilise le même mail
    new_datas = {"email": "mail@mail.com", "test": "Emergency Contact"}
    res, msg = importer.import_line(new_datas)
    assert res.coordonnees_lastname == "lastname"
    assert res.coordonnees_emergency_name == "Emergency Contact"
