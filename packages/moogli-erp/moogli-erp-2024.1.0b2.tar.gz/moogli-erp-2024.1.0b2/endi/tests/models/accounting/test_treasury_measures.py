import pytest
import datetime


@pytest.fixture
def grids(dbsession, company, company2):
    from endi.models.accounting.treasury_measures import TreasuryMeasureGrid

    grids = []

    for year, cid in ((2019, company.id), (2018, company.id), (2017, company2.id)):
        grid = TreasuryMeasureGrid(date=datetime.date(year, 1, 1), company_id=cid)
        dbsession.add(grid)
        grids.append(grid)
    dbsession.flush()
    return grids


class TestTreasuryMeasureGrid:
    def test_get_years(self, grids, company):
        from endi.models.accounting.treasury_measures import (
            TreasuryMeasureGrid,
        )

        assert TreasuryMeasureGrid.get_years() == [2017, 2018, 2019]
        assert TreasuryMeasureGrid.get_years(company.id) == [2018, 2019]

    def test_get_last(self, grids, company, company2):
        from endi.models.accounting.treasury_measures import (
            TreasuryMeasureGrid,
        )

        assert TreasuryMeasureGrid.last(company.id).date.year == 2019
        assert TreasuryMeasureGrid.last(company2.id).date.year == 2017
