import pytest
import datetime


def test_load_value(dbsession):
    from endi.models.config import get_config, Config

    dbsession.add(Config(name="name", value="value"))
    dbsession.flush()
    all_ = get_config()
    assert "name" in list(all_.keys())
    assert all_["name"] == "value"


def test_load_date_value(dbsession):
    from endi.models.config import Config

    dbsession.add(Config(name="datekey", value="2018-01-01"))
    dbsession.flush()

    assert Config.get_value("datekey", type_=datetime.date) == datetime.date(
        2018, 0o1, 0o1
    )

    dbsession.add(Config(name="falsydatekey", value=""))
    dbsession.flush()
    assert Config.get_value("falsydatekey", type_=datetime.date, default="") == ""
    # On teste la valeur par défaut None
    assert Config.get_value("falsydatekey", type_=datetime.date, default=None) is None

    with pytest.raises(ValueError):
        Config.get_value("falsydatekey", type_=datetime.date)


def test_load_int_value(dbsession):
    from endi.models.config import Config

    dbsession.add(Config(name="intkey", value="125"))
    dbsession.flush()

    assert Config.get_value("intkey", type_=int) == 125

    dbsession.add(Config(name="falsyintkey", value=""))
    dbsession.flush()
    assert Config.get_value("falsyintkey", type_=int, default=0) == 0
    assert Config.get_value("falsyintkey", type_=int, default=None) is None

    with pytest.raises(ValueError):
        Config.get_value("falsyintkey", type_=int)


def test_get_value_defaults(dbsession):
    from endi.models.config import Config

    assert Config.get_value("toto") is None
    assert Config.get_value("toto", default=5) == 5
    assert Config.get_value("toto", type_=str) is None
    assert Config.get_value("toto", type_=int) is None

    Config.set("test", "not a num")
    with pytest.raises(ValueError):
        assert Config.get_value("test", type_=int)
