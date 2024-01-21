import pytest


@pytest.fixture
def grids(dbsession, company, company2):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureGrid,
    )

    grids = []

    for year, cid in ((2019, company.id), (2018, company.id), (2017, company2.id)):
        grid = IncomeStatementMeasureGrid(
            year=year,
            month=1,
            company_id=cid,
        )
        dbsession.add(grid)
        grids.append(grid)
    dbsession.flush()
    return grids


class TestIncomeStatementMeasureGrid:
    def test_get_years(self, dbsession, grids, company):
        from endi.models.accounting.income_statement_measures import (
            IncomeStatementMeasureGrid,
        )

        assert IncomeStatementMeasureGrid.get_years() == [2017, 2018, 2019]
        assert IncomeStatementMeasureGrid.get_years(company.id) == [2018, 2019]
