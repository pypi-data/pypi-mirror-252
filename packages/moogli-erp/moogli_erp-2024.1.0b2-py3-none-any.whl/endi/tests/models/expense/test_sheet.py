import datetime
import pytest


class TestExpenseKmLine:
    @pytest.fixture
    def sheet(self, mk_expense_sheet):
        return mk_expense_sheet(year=2018, month=4)

    @pytest.fixture
    def line(self, sheet, mk_expense_type, mk_expense_kmline, project, customer):
        kmtype = mk_expense_type(amount=1, year=2018)
        return mk_expense_kmline(
            description="",
            km=150,
            ht=150,
            expense_type=kmtype,
            start="départ",
            end="arrivée",
            date=datetime.date(2018, 4, 2),
            customer=customer,
            project=project,
            sheet=sheet,
        )

    def test_duplicate(self, sheet, line, mk_expense_sheet, mk_expense_type):
        dup = line.duplicate(sheet)
        for key in (
            "project_id",
            "customer_id",
            "start",
            "end",
            "description",
            "km",
            "ht",
            "date",
        ):
            assert getattr(dup, key) == getattr(line, key)

        sheet2 = mk_expense_sheet(year=2019, month=2)
        dup = line.duplicate(sheet2)
        assert dup is None  # Ref #774

        kmtype2019 = mk_expense_type(amount=1, year=2019)
        dup = line.duplicate(sheet2)
        assert dup.expense_type == kmtype2019
        assert dup.date == datetime.date(2019, 2, 1)


def test_expense_sheet_validation_sets_official_number(
    mk_expense_sheet,
    pyramid_request,
    csrf_request_with_db_and_user,
):
    from endi.models.config import Config

    expense_sheet_1 = mk_expense_sheet()
    expense_sheet_2 = mk_expense_sheet()

    assert expense_sheet_1.official_number is None
    assert expense_sheet_2.official_number is None

    expense_sheet_1.set_status("valid", csrf_request_with_db_and_user)
    assert expense_sheet_1.official_number == "1"

    expense_sheet_2.set_status("valid", csrf_request_with_db_and_user)
    assert expense_sheet_2.official_number == "2"

    # https://framagit.org/endi/endi/-/issues/2596
    Config.set("expensesheet_number_template", "{SEQGLOBAL}-{YYYY}-{YY}-{MM}")
    expense_sheet_3 = mk_expense_sheet(
        year=2021, month=2, status_date=datetime.datetime(2021, 8, 1)
    )
    expense_sheet_3.set_status("valid", csrf_request_with_db_and_user)
    assert expense_sheet_3.official_number == "3-2021-21-02"
