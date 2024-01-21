import pytest
import datetime

from pathlib import Path


@pytest.fixture
def data_dir():
    path = Path(__file__).parent.absolute().joinpath("datas")
    return path


@pytest.fixture
def income_measure_types(dbsession, income_statement_measure_type_categories):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )

    types = []
    for (label, category_index, account_prefix, is_total, total_type) in (
        ("Label 1", 0, "701", False, ""),
        ("Label 2", 0, "701,702", False, ""),
        ("Label 3", 1, "601", False, ""),
        ("Total partiel autres achats", 1, "60,-601", True, "account_prefix"),
        ("Total produits et achats", 1, "Produits,Achats", True, "categories"),
        (
            "Ratio produits et achats",
            1,
            "{Achats} * 100 / {Produits}",
            True,
            "categories",
        ),
        ("Salaires et appointements", 1, "641,-641150", False, ""),
    ):
        typ = IncomeStatementMeasureType(
            label=label,
            category_id=income_statement_measure_type_categories[category_index].id,
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
def mk_operation(dbsession, company):
    from endi.models.accounting.operations import (
        AccountingOperation,
    )

    def factory(
        upload_id,
        general_account="1111111",
        debit=0,
        credit=0,
        label="Test",
        month=None,
        year=None,
        analytical_account=company.code_compta,
        company_id=company.id,
    ):
        options = dict(
            analytical_account=analytical_account,
            general_account=general_account,
            debit=debit,
            credit=credit,
            label=label,
            company_id=company_id,
            upload_id=upload_id,
        )
        if month is not None:
            options["date"] = datetime.date(year, month, 1)

        op = AccountingOperation(**options)
        dbsession.add(op)
        dbsession.flush()
        return op

    return factory


@pytest.fixture
def analytical_upload(dbsession):
    from endi.models.accounting.operations import AccountingOperationUpload

    item = AccountingOperationUpload(
        md5sum="oooo",
        filetype="analytical_balance",
        date=datetime.date.today(),
    )
    dbsession.add(item)
    return item


@pytest.fixture
def analytical_operations(dbsession, analytical_upload, mk_operation):
    operations = []
    for general, label, debit, credit in (
        ("50000", "depot banque 1", 1000, 0),
        ("51000", "depo banque 2", 1000, 0),
        ("42000", "cotisation", 0, 1000),
        ("425000", "dépenses", 0, 1000),
    ):
        operations.append(
            mk_operation(
                general_account=general,
                label=label,
                debit=debit,
                credit=credit,
                upload_id=analytical_upload.id,
            )
        )
    return operations


@pytest.fixture
def general_upload(dbsession):
    from endi.models.accounting.operations import AccountingOperationUpload

    item = AccountingOperationUpload(
        md5sum="oooo",
        filetype="general_ledger",
        date=datetime.date.today(),
    )
    dbsession.add(item)
    return item


@pytest.fixture
def general_operations(dbsession, general_upload, mk_operation):
    operations = []
    for month, general, label, debit, credit in (
        (1, "70100", "", 1000, 0),
        (1, "70200", "", 1000, 0),
        (1, "602", "avoir", 0, 1000),
        (1, "601", "achats", 0, 1000),
        (1, "641150", "Test", 0, 17370),
        (1, "641", "Test", 5625, 0),
        (2, "70100", "", 2000, 0),
        (2, "70200", "", 2000, 0),
        (2, "602", "avoir", 0, 2000),
        (2, "601", "achats", 0, 2000),
        (2, "641", "Test", 38521.11, 0),
    ):
        operations.append(
            mk_operation(
                general_upload.id,
                general,
                debit,
                credit,
                label,
                month=month,
                year=2017,
            )
        )
    return operations


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
def mk_income_statement_measure_grid(dbsession, company):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureGrid,
    )

    def factory(year, month, company_id=company.id):
        inst = IncomeStatementMeasureGrid(year=year, month=month, company_id=company_id)
        dbsession.add(inst)
        dbsession.flush()
        return inst

    return factory


@pytest.fixture
def mk_income_statement_measure(dbsession):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasure,
    )

    def factory(grid, label, measure_type, value=0):
        inst = IncomeStatementMeasure(
            grid_id=grid.id,
            label=label,
            measure_type_id=measure_type.id,
            value=value,
        )
        dbsession.add(inst)
        dbsession.flush()
        return inst

    return factory
