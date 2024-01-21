import pytest
import datetime


@pytest.fixture
def income_statement_measure_types(dbsession, income_statement_measure_type_categories):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )

    types = []
    for (label, category_index, account_prefix, is_total, total_type) in (
        ("Label 1", 0, "701", False, ""),
        ("Label 2", 0, "701,702", False, ""),
        ("Label 3", 1, "601", False, ""),
        ("Total partiel autres achats", 1, "6,-601", True, "account_prefix"),
        ("Total produits et achats", 1, "Produits,Achats", True, "categories"),
        (
            "Ratio produits et achats",
            1,
            "{Achats} * 100 / {Produits}",
            True,
            "complex_total",
        ),
        (
            "Formule de test",
            1,
            "({Label 1} + {Label 2} + {Label 3})",
            True,
            "complex_total",
        ),
    ):
        cid = income_statement_measure_type_categories[category_index].id
        typ = IncomeStatementMeasureType(
            label=label,
            category_id=cid,
            account_prefix=account_prefix,
            is_total=is_total,
            total_type=total_type,
        )
        dbsession.add(typ)
        typ.category = income_statement_measure_type_categories[category_index]
        types.append(typ)
    return types


@pytest.fixture
def treasury_measure_type_categories(dbsession):
    from endi.models.accounting.treasury_measures import (
        TreasuryMeasureTypeCategory,
    )

    categories = []
    for order, name in enumerate(["Référence", "Future", "Autres"]):
        category = TreasuryMeasureTypeCategory(label=name, order=order)
        dbsession.add(category)
        categories.append(category)
    dbsession.flush()
    return categories


@pytest.fixture
def treasury_measure_types(dbsession, treasury_measure_type_categories):
    from endi.models.accounting.treasury_measures import (
        TreasuryMeasureType,
    )

    types = [
        (0, "5", "Trésorerie du jour", True, "account_prefix"),
        (0, "42,-421,-425,43,44", "Impôts, taxes et cotisations dues", False, None),
        (0, "40", "Fournisseurs à payer", False, None),
        (0, "Référence", "Trésorerie de référence", True, "categories"),
        (1, "421", "Salaires à payer", False, None),
        (1, "41", "Clients à encaisser", False, None),
        (1, "425", "Notes de dépenses à payer", False, None),
        (1, "{Référence}+{Future}", "Trésorerie future", True, "complex_total"),
        (2, "1,2,3", "Comptes bilan non pris en compte", False, None),
        (
            2,
            "{Référence}+{Future}+{Autres}",
            "Résultat de l'enseigne",
            True,
            "complex_total",
        ),
    ]
    result = []
    for order, data in enumerate(types):
        (category_index, account_prefix, label, is_total, total_type) = data
        category_id = treasury_measure_type_categories[category_index].id
        typ = TreasuryMeasureType(
            category_id=category_id,
            account_prefix=account_prefix,
            label=label,
            is_total=is_total,
            order=order,
            total_type=total_type,
        )
        dbsession.add(typ)
        result.append(typ)
    typ = TreasuryMeasureType(
        category_id=category_id, account_prefix="21", label="Unactive one", active=False
    )
    dbsession.add(typ)
    result.append(typ)
    return result


@pytest.fixture
def income_statement_measures(
    dbsession,
    income_statement_measure_types,
):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasure,
    )

    result = []
    for index, value in enumerate((-8000, -2000, +1000, +500, -8500, 15, -9000)):
        typ_ = income_statement_measure_types[index]
        mes = IncomeStatementMeasure(
            label=typ_.label, value=value, measure_type_id=typ_.id
        )
        dbsession.add(mes)
        result.append(mes)
    dbsession.flush()
    return result


@pytest.fixture
def income_statement_measure_grid(
    dbsession,
    company,
    income_statement_measures,
):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureGrid,
    )

    grid = IncomeStatementMeasureGrid(
        company_id=company.id,
        year=2018,
        month=3,
    )
    grid.measures = income_statement_measures
    dbsession.add(grid)
    dbsession.flush()
    return grid


@pytest.fixture
def mk_treasury_measure_grid(dbsession, company):
    from endi.models.accounting.treasury_measures import (
        TreasuryMeasureGrid,
    )

    def factory(date, company_id=company.id):
        inst = TreasuryMeasureGrid(date=date, company_id=company_id)
        dbsession.add(inst)
        dbsession.flush()
        return inst

    return factory


@pytest.fixture
def mk_treasury_measure(dbsession):
    from endi.models.accounting.treasury_measures import (
        TreasuryMeasure,
    )

    def factory(grid, label, measure_type, value=0):
        inst = TreasuryMeasure(
            grid_id=grid.id,
            label=label,
            measure_type_id=measure_type.id,
            value=value,
        )
        dbsession.add(inst)
        dbsession.flush()
        return inst

    return factory


@pytest.fixture
def treasury_measure_grid(
    dbsession,
    mk_treasury_measure_grid,
    mk_treasury_measure,
    treasury_measure_types,
):
    import datetime

    grid = mk_treasury_measure_grid(datetime.date.today())
    for index, value in enumerate([13000, 14469, 10676, 25145, 7247, -582, 3621]):
        mk_treasury_measure(
            grid=grid,
            label="index %s" % index,
            measure_type=treasury_measure_types[index],
            value=value,
        )
    dbsession.merge(grid)
    dbsession.flush()
    return grid


@pytest.fixture
def synchronized_upload(dbsession):
    from endi.models.accounting.operations import AccountingOperationUpload

    res = AccountingOperationUpload(
        filetype=AccountingOperationUpload.SYNCHRONIZED_ACCOUNTING,
        filename="Écritures 2017",
        date=datetime.date(2017, 1, 1),
        created_at=datetime.date.today(),
    )
    dbsession.add(res)
    dbsession.flush()
    return res
