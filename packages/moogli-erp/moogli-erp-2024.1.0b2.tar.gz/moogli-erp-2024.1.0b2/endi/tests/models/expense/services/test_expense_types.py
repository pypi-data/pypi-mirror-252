from unittest.mock import Mock
import pytest

from endi.models.expense.services import ExpenseTypeService


@pytest.fixture
def active_expense_type(mk_expense_type):
    return mk_expense_type("ET1", 1)


@pytest.fixture
def inactive_expense_type(mk_expense_type):
    return mk_expense_type("ET2", 2, active=False)


def test_active_or_used_in(active_expense_type, inactive_expense_type):
    assert ExpenseTypeService.active_or_used_in().all() == [active_expense_type]

    objs = [Mock(type_id=inactive_expense_type.id)]
    assert ExpenseTypeService.active_or_used_in(objs).all() == [
        active_expense_type,
        inactive_expense_type,
    ]

    objs_bis = [Mock(type_id=inactive_expense_type.id)]
    assert ExpenseTypeService.active_or_used_in(objs, objs_bis).all() == [
        active_expense_type,
        inactive_expense_type,
    ]


@pytest.fixture
def active_expensekm_type(mk_expense_type):
    return mk_expense_type(
        label="Déplacement cat1",
        code="cat1",
        amount=10,
    )


@pytest.fixture
def active_expensekm_type_issue_2098(mk_expense_type):
    return mk_expense_type(
        label="Déplacement - cat1",
        code="cat1",
        amount=10,
    )


@pytest.fixture
def inactive_expensekm_type(mk_expense_type):
    return mk_expense_type(
        label="Déplacement cat2",
        code="cat2",
        amount=10,
        active=False,
    )


@pytest.fixture
def unrestricted_user(user):
    return user


@pytest.fixture
def restricted_user_cat2(mk_user):
    # Restricted to cat2, which is disabled
    return mk_user(
        lastname="Restricted Lastname",
        firstname="Restricted Firstname",
        email="restricted@c.fr",
        vehicle="Déplacement cat2-cat2",
    )


@pytest.fixture
def restricted_user_cat1(mk_user):
    # Restricted to cat2, which is disabled
    return mk_user(
        lastname="Restricted Lastname",
        firstname="Restricted Firstname",
        email="restricted@c.fr",
        vehicle="Déplacement cat1-cat1",
    )


@pytest.fixture
def restricted_user_cat1_issue_2098(mk_user):
    # Restricted to cat2, which is disabled
    return mk_user(
        lastname="Restricted Lastname",
        firstname="Restricted Firstname",
        email="restricted@c.fr",
        vehicle="Déplacement - cat1-cat1",
    )


def test_allowed_driver(
    unrestricted_user,
    restricted_user_cat1,
    restricted_user_cat1_issue_2098,
    restricted_user_cat2,
    active_expensekm_type,
    active_expensekm_type_issue_2098,
    inactive_expense_type,
):
    assert ExpenseTypeService.allowed_driver(unrestricted_user, 2018).all() == [
        active_expensekm_type,
        active_expensekm_type_issue_2098,
    ]

    # It has only the disabled expensetype allowed, thus, nothing available
    assert ExpenseTypeService.allowed_driver(restricted_user_cat2, 2018).all() == []

    assert ExpenseTypeService.allowed_driver(restricted_user_cat1, 2018).all() == [
        active_expensekm_type
    ]
    assert ExpenseTypeService.allowed_driver(
        restricted_user_cat1_issue_2098, 2018
    ).all() == [active_expensekm_type_issue_2098]


def test_allowed_driver_or_used_in(
    unrestricted_user,
    restricted_user_cat1,
    restricted_user_cat2,
    active_expensekm_type,
    inactive_expense_type,
):
    assert ExpenseTypeService.allowed_driver_or_used_in(
        restricted_user_cat2, 2018, [Mock(type_id=inactive_expense_type.id)]
    ).all() == [inactive_expense_type]

    assert (
        ExpenseTypeService.allowed_driver_or_used_in(
            restricted_user_cat2, 2018, []
        ).all()
        == []
    )
