import pytest
from endi.models.third_party.third_party import ThirdParty


@pytest.fixture
def mk_tp(fixture_factory, company):
    return fixture_factory(
        ThirdParty,
        company_name="company_tp",
        type="company",
        code="CUST",
        lastname="Lastname",
        firstname="Firstname",
        address="1th street",
        additional_address="1st floor",
        zip_code="01234",
        city="City",
        company_id=company.id,
    )


@pytest.fixture
def company_tp(mk_tp):
    return mk_tp()


@pytest.fixture
def individual_tp(mk_tp):
    return mk_tp(type="individual", civilite="mr&mme")


@pytest.fixture
def internal_tp(mk_tp, company2):
    return mk_tp(
        source_company=company2,
        type="internal",
    )


def test_company_address(company_tp):
    assert (
        company_tp.full_address
        == """company_tp\nLastname Firstname\n1th street\n1st floor\n01234 City"""
    )
    company_tp.country = "England"
    assert (
        company_tp.full_address
        == """company_tp\nLastname Firstname\n1th street\n1st floor\n01234 City\nEngland"""
    )


def test_individual_address(individual_tp):
    assert (
        individual_tp.full_address
        == """M. et Mme Lastname Firstname\n1th street\n1st floor\n01234 City"""
    )


def test_label_company(company_tp):
    # Property label is persisted in name
    assert company_tp.label == company_tp.name
    # label is company_name
    assert company_tp.name == company_tp.company_name


def test_label_individual(dbsession, individual_tp):
    # Property label is persisted in name
    assert individual_tp.label == individual_tp.name
    # label is company_name
    assert individual_tp.label == """M. et Mme Lastname Firstname"""
    individual_tp.civilite = None
    dbsession.merge(individual_tp)
    dbsession.flush()
    assert individual_tp.label == """Lastname Firstname"""


def test_label_internal(internal_tp):
    # Property label is persisted in name
    assert internal_tp.label == internal_tp.name
    # label is company_name
    assert internal_tp.label == internal_tp.company_name


def test_from_company(company, company2, company3, user, login, mk_config):
    company.employees.append(user)
    mk_config("cae_address", "1 rue victor hugo")
    mk_config("cae_zipcode", "23000")
    mk_config("cae_city", "Guéret")
    result = ThirdParty.from_company(company, company2)

    assert result.type == "internal"
    assert result.company_name == company.name
    assert result.email == company.email
    assert result.lastname == user.lastname
    assert result.firstname == user.firstname
    assert result.civilite == user.civilite
    assert result.source_company_id == company.id
    assert result.address == "1 rue victor hugo"
    assert result.zip_code == "23000"
    assert result.city == "Guéret"
    assert result.company_id == company2.id
    # Test no duplicate
    new_result = ThirdParty.from_company(company, company2)
    assert result == new_result
    # Test different owner
    new_result = ThirdParty.from_company(company, company3)
    assert new_result != result
