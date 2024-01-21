import datetime

from freezegun import freeze_time
import pytest

from endi.models.supply.supplier_order import get_supplier_orders_years


@pytest.fixture
def order_2017(mk_supplier_order):
    mk_supplier_order(created_at=datetime.date(2017, 10, 10))


@pytest.fixture
def order_2017bis(mk_supplier_order):
    mk_supplier_order(created_at=datetime.date(2017, 1, 1))


@pytest.fixture
def order_2018(mk_supplier_order):
    mk_supplier_order(created_at=datetime.date(2018, 1, 1))


# Use several tests to invalidate cache between tests


@freeze_time("2019")
def test_get_supplier_orders_years_no_order(
    dbsession,
):
    assert get_supplier_orders_years() == [2019]


@freeze_time("2019")
def test_get_supplier_orders_years_one_order(order_2017):
    assert get_supplier_orders_years() == [2017, 2019]


@freeze_time("2019")
def test_get_supplier_orders_years_two_orders_same_year(order_2017, order_2017bis):
    assert get_supplier_orders_years() == [2017, 2019]


@freeze_time("2019")
def test_get_supplier_orders_years_three_orders_different_year(
    order_2017,
    order_2017bis,
    order_2018,
):
    assert get_supplier_orders_years() == [2017, 2018, 2019]


def test_line_from_task(
    mk_task_line,
    mk_internalestimation,
    mk_tva,
    mk_expense_type,
    task_line_group,
    dbsession,
):
    line = mk_task_line(
        tva=0,
        cost=15021000,
        quantity=2,
        group=task_line_group,
    )
    estimation = mk_internalestimation(
        description="Description",
    )
    task_line_group.lines = [line]
    estimation.line_groups = [task_line_group]
    dbsession.merge(estimation)
    dbsession.flush()

    from endi.models.supply.supplier_order import SupplierOrderLine

    oline = SupplierOrderLine.from_task(estimation)
    assert oline.ht == 30042
    assert oline.tva == 0
    assert oline.description == "Description"
    assert oline.type_id is None

    typ = mk_expense_type(label="type interne", internal=True)
    oline = SupplierOrderLine.from_task(estimation)
    assert oline.type_id == typ.id
