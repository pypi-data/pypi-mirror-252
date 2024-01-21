import datetime
from endi.tests.tools import Dummy


class TestBaseMeasureCompiler:
    def test_collect_common_measure_types(self, treasury_measure_types):
        from endi_celery.tasks.accounting_measure_compute import TreasuryMeasureCompiler

        upload = Dummy(filetype="test")
        compiler = TreasuryMeasureCompiler(upload, None)

        expected = (
            treasury_measure_types[0:3]
            + treasury_measure_types[4:7]
            + [treasury_measure_types[8]]
        )
        assert compiler._collect_common_measure_types() == expected

    def test_collect_computed_measure_types(
        self,
        treasury_measure_types,
        treasury_measure_type_categories,
    ):
        from endi_celery.tasks.accounting_measure_compute import TreasuryMeasureCompiler
        from collections import OrderedDict

        upload = Dummy(filetype="test")
        compiler = TreasuryMeasureCompiler(upload, None)
        expected = OrderedDict()

        expected[treasury_measure_type_categories[0].id] = [treasury_measure_types[3]]
        expected[treasury_measure_type_categories[1].id] = [treasury_measure_types[7]]
        expected[treasury_measure_type_categories[2].id] = [treasury_measure_types[9]]
        assert compiler._collect_computed_measure_types() == expected

    def test_collect_categories(self, treasury_measure_type_categories):
        from endi_celery.tasks.accounting_measure_compute import TreasuryMeasureCompiler

        upload = Dummy(filetype="test")
        compiler = TreasuryMeasureCompiler(upload, None)

        assert compiler._collect_categories() == treasury_measure_type_categories


class TestTreasuryMeasureCompiler:
    def getOne(self, analytical_upload, analytical_operations):
        from endi_celery.tasks.accounting_measure_compute import (
            TreasuryMeasureCompiler,
        )

        return TreasuryMeasureCompiler(analytical_upload, analytical_operations)

    def get_cache_key_from_operation(
        self,
    ):
        from endi.models.accounting.operations import (
            AccountingOperationUpload,
        )

        today = datetime.date.today()
        upload = Dummy(
            id=1,
            date=today,
            operations=[],
            filetype=AccountingOperationUpload.SYNCHRONIZED_ACCOUNTING,
        )
        compiler = self.getOne(upload, [])
        operation = Dummy(upload=upload, company_id=2)
        key = compiler.get_cache_key_from_operation(operation)
        assert key == (2, today)
        upload.filetype = "other"
        key = compiler.get_cache_key_from_operation(operation)
        assert key == (2, today)

    def test_get_grid_item(
        self,
        dbsession,
        mk_treasury_measure_grid,
        analytical_upload,
        mk_operation,
        company2,
    ):
        # On vérifie si la grid renvoyée est bien concernée par l'opération
        # passée en param (company_id, upload.date)
        # mk_treasury_measure_grid(analytical_upload.date)
        grid = mk_treasury_measure_grid(analytical_upload.date)
        compiler = self.getOne(analytical_upload, [])
        # OK
        operation = mk_operation(analytical_upload.id)
        assert compiler.get_grid_item(operation).grid == grid

    def test_process_common_measures_treasury(
        self,
        dbsession,
        analytical_upload,
        analytical_operations,
        treasury_measure_types,
        treasury_measure_type_categories,
        company,
    ):
        compiler = self.getOne(analytical_upload, analytical_operations)
        grid_items = compiler._process_common_measures()

        grids = [g.grid for g in grid_items]
        assert len(grids) == 1
        assert grids[0].date == analytical_upload.date

        grid = grids[0]
        assert grid.company_id == company.id
        for type_index, value in (
            (0, 2000),
            (1, -1000),
            (6, -1000),
        ):
            measure_type = treasury_measure_types[type_index]
            assert grid.get_measure_by_type(measure_type.id).value == value

    def test_cache_grid_totals_treasury(
        self,
        dbsession,
        analytical_upload,
        analytical_operations,
        treasury_measure_types,
        treasury_measure_type_categories,
        company,
    ):
        compiler = self.getOne(analytical_upload, analytical_operations)
        grid_items = compiler._process_common_measures()
        compiler._cache_grid_totals()
        grid_item = grid_items[0]
        for type_index, value in (
            (0, 2000),
            (1, -1000),
            (6, -1000),
        ):
            measure_type = treasury_measure_types[type_index]
            assert grid_item._type_totals[measure_type.id] == value

        for category_index, value in (
            (0, 1000),
            (1, -1000),
        ):
            category = treasury_measure_type_categories[category_index]
            assert grid_item._category_totals[category.id] == value


class TestIncomeStatementMeasureCompiler:
    def getOne(self, general_upload, general_operations):
        from endi_celery.tasks.accounting_measure_compute import (
            IncomeStatementMeasureCompiler,
        )

        return IncomeStatementMeasureCompiler(general_upload, general_operations)

    def test_get_grid_item(
        self,
        dbsession,
        mk_income_statement_measure_grid,
        general_upload,
        mk_operation,
        company2,
    ):
        # On vérifie si la grid renvoyée est bien concernée par l'opération
        # passée en param (year, month, company_id)
        grid = mk_income_statement_measure_grid(2017, 1)
        compiler = self.getOne(general_upload, [])
        # OK
        operation = mk_operation(general_upload.id, month=1, year=2017)
        assert compiler.get_grid_item(operation).grid == grid
        # != year
        operation = mk_operation(general_upload.id, month=1, year=2018)
        assert compiler.get_grid_item(operation).grid != grid
        # != month
        operation = mk_operation(general_upload.id, month=2, year=2017)
        assert compiler.get_grid_item(operation).grid != grid
        # != company_id
        operation = mk_operation(
            general_upload.id, month=1, year=2017, company_id=company2.id
        )
        assert compiler.get_grid_item(operation).grid != grid

    def test_process_common_measures_income_statement(
        self,
        dbsession,
        general_upload,
        general_operations,
        income_measure_types,
        income_statement_measure_type_categories,
        company,
    ):
        compiler = self.getOne(general_upload, general_operations)
        grid_items = compiler._process_common_measures()
        grids = [g.grid for g in grid_items]
        grids = sorted(grids, key=lambda i: i.month)

        assert len(grids) == 2

        assert grids[0].month == 1
        assert grids[0].year == 2017

        assert grids[1].month == 2
        assert grids[1].year == 2017

        grid = grids[0]

        assert grid.company_id == company.id
        assert len(grid.measures) == 5
        for type_index, value in (
            (0, -1000),
            (1, -2000),
            (2, 1000),
            (3, 1000),
            (6, -5625),
        ):
            measure_type = income_measure_types[type_index]
            assert grid.get_measure_by_type(measure_type.id).value == value

    def test_cache_grid_totals_income_statement(
        self,
        dbsession,
        general_upload,
        general_operations,
        income_measure_types,
        income_statement_measure_type_categories,
        company,
    ):
        compiler = self.getOne(general_upload, general_operations)
        grid_items = compiler._process_common_measures()
        compiler._cache_grid_totals()
        grid_item = grid_items[0]
        for type_index, value in (
            (0, -1000),
            (1, -2000),
            (2, 1000),
            (3, 1000),
            (6, -5625),
        ):
            measure_type = income_measure_types[type_index]
            assert grid_item._type_totals[measure_type.id] == value

        for category_index, value in (
            (0, -3000),
            (1, -3625),
        ):
            category = income_statement_measure_type_categories[category_index]
            assert grid_item._category_totals[category.id] == value
