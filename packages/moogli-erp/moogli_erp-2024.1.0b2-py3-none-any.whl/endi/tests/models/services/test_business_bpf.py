import pytest

from endi.models.services.bpf import BusinesssBPFDataMigrator_15to16
from endi.models.training.bpf import (
    IncomeSource,
    TraineeCount,
)


@pytest.fixture
def mk_income_source(fixture_factory, invoice):
    return fixture_factory(
        IncomeSource,
        invoice_id=invoice.id,
        income_category_id=1,
    )


@pytest.fixture
def mk_trainee_count(
    fixture_factory,
):
    return fixture_factory(
        TraineeCount,
        trainee_type_id=1,
        headcount=10,
        total_hours=100,
    )


@pytest.fixture
def bpf_data_wrong_cerfa_full(
    mk_business_bpf_data,
    mk_income_source,
    mk_trainee_count,
    training_business,
):
    bpf_data = mk_business_bpf_data(
        financial_year=2020,
        cerfa_version="10443*15",
        training_goal_id=8,
        business=training_business,
    )
    mk_income_source(business_bpf_data_id=bpf_data.id)
    mk_trainee_count(business_bpf_data_id=bpf_data.id)
    return bpf_data


def test_BusinesssBPFDataMigrator_15to16(bpf_data_wrong_cerfa_full):
    bpf_data = bpf_data_wrong_cerfa_full

    BusinesssBPFDataMigrator_15to16.migrate(bpf_data)

    assert bpf_data.cerfa_version == "10443*16"
    assert bpf_data.financial_year == 2020
    assert len(bpf_data.income_sources) == 1
    assert bpf_data.income_sources[0].income_category_id == 2
    assert len(bpf_data.trainee_types) == 1
    assert bpf_data.trainee_types[0].trainee_type_id == 2

    assert bpf_data.training_goal_id == 14


@pytest.fixture
def bpf_data_query_2021():
    from endi.models.training.bpf import BusinessBPFData
    from endi.models.project.business import Business

    return (
        BusinessBPFData.query()
        .join(Business.query().subquery(with_labels=True))
        .filter(
            BusinessBPFData.financial_year == 2021,
        )
    )


@pytest.fixture
def bpf_data_2021_not_subcontract(
    mk_business_bpf_data,
    mk_income_source,
    mk_trainee_count,
    training_business,
):
    bpf_data = mk_business_bpf_data(
        financial_year=2021,
        cerfa_version="10443*16",
        training_goal_id=5,
        business=training_business,
        is_subcontract=False,
    )
    mk_income_source(business_bpf_data_id=bpf_data.id)
    mk_trainee_count(business_bpf_data_id=bpf_data.id)
    return bpf_data


@pytest.fixture
def bpf_data_2021_subcontract(
    mk_business_bpf_data,
    mk_income_source,
    mk_trainee_count,
    training_business,
):
    bpf_data = mk_business_bpf_data(
        financial_year=2021,
        cerfa_version="10443*16",
        training_goal_id=5,
        business=training_business,
        is_subcontract=True,
    )
    mk_income_source(business_bpf_data_id=bpf_data.id)
    mk_trainee_count(business_bpf_data_id=bpf_data.id)
    return bpf_data


def test_bpf_data_subcontract_f_tab_bug3516(
    bpf_data_2021_subcontract,
    bpf_data_query_2021,
):
    from endi.models.services.bpf import Cerfa_10443_16

    data_dict = Cerfa_10443_16.build_data_dict(bpf_data_query_2021)

    assert data_dict["f_1_ligne_a_nb"] == 0
    assert data_dict["f_1_ligne_b_nb"] == 0
    assert data_dict["f_1_ligne_c_nb"] == 0
    assert data_dict["f_1_ligne_d_nb"] == 0
    assert data_dict["f_1_ligne_e_nb"] == 0
    assert data_dict["f_1_ligne_a_h"] == 0
    assert data_dict["f_1_ligne_b_h"] == 0
    assert data_dict["f_1_ligne_c_h"] == 0
    assert data_dict["f_1_ligne_d_h"] == 0
    assert data_dict["f_1_ligne_e_h"] == 0
    assert data_dict["f_1_ligne_1bis_nb"] == 0
    assert data_dict["f_2_ligne_2_nb"] == 0
    assert data_dict["f_2_ligne_2_c"] == 0
    assert data_dict["f_3_ligne_a1_nb"] == 0
    assert data_dict["f_3_ligne_a2_nb"] == 0
    assert data_dict["f_3_ligne_a3_nb"] == 0
    assert data_dict["f_3_ligne_a4_nb"] == 0
    assert data_dict["f_3_ligne_a5_nb"] == 0
    assert data_dict["f_3_ligne_a6_nb"] == 0
    assert data_dict["f_3_ligne_b_nb"] == 0
    assert data_dict["f_3_ligne_c_nb"] == 0
    assert data_dict["f_3_ligne_d_nb"] == 0
    assert data_dict["f_3_ligne_e_nb"] == 0
    assert data_dict["f_3_ligne_f_nb"] == 0
    assert data_dict["f_3_ligne_a1_h"] == 0
    assert data_dict["f_3_ligne_a2_h"] == 0
    assert data_dict["f_3_ligne_a3_h"] == 0
    assert data_dict["f_3_ligne_a4_h"] == 0
    assert data_dict["f_3_ligne_a5_h"] == 0
    assert data_dict["f_3_ligne_a6_h"] == 0
    assert data_dict["f_3_ligne_b_h"] == 0
    assert data_dict["f_3_ligne_c_h"] == 0
    assert data_dict["f_3_ligne_d_h"] == 0
    assert data_dict["f_3_ligne_e_h"] == 0
    assert data_dict["f_3_ligne_f_h"] == 0
    assert len(list(data_dict["f_4"])) == 0


def test_bpf_data_not_subcontract_f_tab_bug3516(
    bpf_data_2021_not_subcontract,
    bpf_data_query_2021,
):
    from endi.models.services.bpf import Cerfa_10443_16

    data_dict = Cerfa_10443_16.build_data_dict(bpf_data_query_2021)

    assert data_dict["f_1_ligne_a_nb"] == 0
    assert data_dict["f_1_ligne_b_nb"] == 10
    assert data_dict["f_1_ligne_c_nb"] == 0
    assert data_dict["f_1_ligne_d_nb"] == 0
    assert data_dict["f_1_ligne_e_nb"] == 0
    assert data_dict["f_1_ligne_a_h"] == 0
    assert data_dict["f_1_ligne_b_h"] == 100
    assert data_dict["f_1_ligne_c_h"] == 0
    assert data_dict["f_1_ligne_d_h"] == 0
    assert data_dict["f_1_ligne_e_h"] == 0
    assert data_dict["f_1_ligne_1bis_nb"] == 0
    assert data_dict["f_2_ligne_2_nb"] == 0
    assert data_dict["f_2_ligne_2_c"] == 0
    assert data_dict["f_3_ligne_a1_nb"] == 0
    assert data_dict["f_3_ligne_a2_nb"] == 0
    assert data_dict["f_3_ligne_a3_nb"] == 0
    assert data_dict["f_3_ligne_a4_nb"] == 0
    assert data_dict["f_3_ligne_a5_nb"] == 0
    assert data_dict["f_3_ligne_a6_nb"] == 10
    assert data_dict["f_3_ligne_b_nb"] == 0
    assert data_dict["f_3_ligne_c_nb"] == 0
    assert data_dict["f_3_ligne_d_nb"] == 0
    assert data_dict["f_3_ligne_e_nb"] == 0
    assert data_dict["f_3_ligne_f_nb"] == 0
    assert data_dict["f_3_ligne_a1_h"] == 0
    assert data_dict["f_3_ligne_a2_h"] == 0
    assert data_dict["f_3_ligne_a3_h"] == 0
    assert data_dict["f_3_ligne_a4_h"] == 0
    assert data_dict["f_3_ligne_a5_h"] == 0
    assert data_dict["f_3_ligne_a6_h"] == 100
    assert data_dict["f_3_ligne_b_h"] == 0
    assert data_dict["f_3_ligne_c_h"] == 0
    assert data_dict["f_3_ligne_d_h"] == 0
    assert data_dict["f_3_ligne_e_h"] == 0
    assert data_dict["f_3_ligne_f_h"] == 0
    assert len(list(data_dict["f_4"])) == 1
