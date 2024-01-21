from endi.tests.tools import Dummy


class TestTreasuryMeasureCompute:
    def getOne(self, grid):
        from endi.views.accounting.treasury_measures import (
            TreasuryGridCompute,
        )

        return TreasuryGridCompute(grid)

    def test_compile_rows(self, treasury_measure_grid):
        wrapper = self.getOne(treasury_measure_grid)
        assert len(wrapper.rows) == 7

        assert wrapper.rows[0][1] == 13000
