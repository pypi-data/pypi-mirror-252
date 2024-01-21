import datetime
from pytest import fixture


@fixture
def expense_kmline(dbsession, mk_expense_type):
    typ = mk_expense_type(label="KM", code="KM", amount=1.254, year=2018)
    from endi.models.expense.sheet import ExpenseKmLine

    item = ExpenseKmLine(
        description="Aller retour",
        category="1",
        type_id=typ.id,
        km=10000,
        ht=10000 * typ.amount,
        start="Dijon",
        end="Lyon",
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def expense_telline(dbsession, mk_expense_type):
    typ = mk_expense_type(percentage=50)
    from endi.models.expense.sheet import ExpenseLine

    item = ExpenseLine(
        description="Test expense",
        category="1",
        type_id=typ.id,
        ht=3000,
        tva=600,
    )
    dbsession.add(item)
    dbsession.flush()
    return item


@fixture
def expense_line(dbsession, mk_expense_line):
    return mk_expense_line()


@fixture
def full_expense_sheet(
    mk_expense_sheet,
    expense_line,
    expense_kmline,
    expense_telline,
    dbsession,
):
    expense_sheet = mk_expense_sheet(
        status_date=datetime.datetime(2019, 1, 1),
    )
    expense_sheet.lines.append(expense_line)
    expense_sheet.lines.append(expense_telline)
    expense_sheet.kmlines.append(expense_kmline)
    dbsession.merge(expense_sheet)
    dbsession.flush()
    return expense_sheet
