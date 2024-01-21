class TestYearGlobalGrid:
    def get_global_grid(self, year, grids=(), turnover=10000):
        from endi.views.accounting.income_statement_measures import (
            YearGlobalGrid,
        )

        return YearGlobalGrid(year=year, grids=grids, turnover=turnover)

    def get_grid_query(self, year, company_id):
        from sqlalchemy import orm, or_, and_
        from endi.models.accounting.income_statement_measures import (
            IncomeStatementMeasureGrid,
        )
        from endi.utils.accounting import get_financial_year_data

        financial_year = get_financial_year_data(year)

        query = IncomeStatementMeasureGrid.query()
        query = query.options(
            orm.joinedload(IncomeStatementMeasureGrid.measures, innerjoin=True)
        )
        query = query.filter(IncomeStatementMeasureGrid.company_id == company_id)
        query = query.filter(
            or_(
                and_(
                    IncomeStatementMeasureGrid.year == financial_year["start_year"],
                    IncomeStatementMeasureGrid.month >= financial_year["start_month"],
                ),
                and_(
                    IncomeStatementMeasureGrid.year == financial_year["end_year"],
                    IncomeStatementMeasureGrid.month <= financial_year["end_year"],
                ),
            )
        )
        query = query.order_by(
            IncomeStatementMeasureGrid.year, IncomeStatementMeasureGrid.month
        )
        return query

    def test_grid_columns_index(self, income_statement_measure_grid):
        from endi.models.config import Config

        year = income_statement_measure_grid.year
        company_id = income_statement_measure_grid.company_id

        grid_query = self.get_grid_query(year, company_id)
        grid = self.get_global_grid(year, grid_query)
        assert grid.columns_index[1] == (year, 1)
        assert grid.columns_index[12] == (year, 12)

        Config.set("accounting_closure_day", 30)
        Config.set("accounting_closure_month", 9)
        grid_query = self.get_grid_query(year, company_id)
        grid = self.get_global_grid(year, grid_query)
        assert grid.columns_index[1] == (year - 1, 10)
        assert grid.columns_index[12] == (year, 9)

    def test_compile_rows(
        self,
        income_statement_measure_type_categories,
        income_statement_measure_types,
        income_statement_measure_grid,
    ):
        grid_query = self.get_grid_query(
            income_statement_measure_grid.year,
            income_statement_measure_grid.company_id,
        )
        global_grid = self.get_global_grid(
            income_statement_measure_grid.year,
            grid_query,
            turnover=10000,
        )

        assert global_grid.rows[0] == (
            income_statement_measure_types[0],
            False,
            [0, 0, -8000, 0, 0, 0, 0, 0, 0, 0, 0, 0, -8000, -80],
        )
        assert global_grid.rows[1] == (
            income_statement_measure_types[1],
            False,
            [0, 0, -2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2000, -20],
        )
        assert global_grid.rows[2] == (
            income_statement_measure_types[2],
            False,
            [0, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 10],
        )
        assert global_grid.rows[3] == (
            income_statement_measure_types[3],
            False,
            [0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 500, 5],
        )
        assert global_grid.rows[4] == (
            income_statement_measure_types[4],
            False,
            [0, 0, -8500, 0, 0, 0, 0, 0, 0, 0, 0, 0, -8500, -85],
        )
        assert global_grid.rows[5] == (
            income_statement_measure_types[5],
            False,
            [0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 0.15],
        )
        assert global_grid.rows[6] == (
            income_statement_measure_types[6],
            False,
            [0, 0, -9000, 0, 0, 0, 0, 0, 0, 0, 0, 0, -9000, -90],
        )
