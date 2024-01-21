import pytest


@pytest.fixture
def measure_type_category(dbsession):
    from endi.models.accounting.base import BaseAccountingMeasureTypeCategory

    cat = BaseAccountingMeasureTypeCategory(label="label_1", order=1)
    dbsession.add(cat)
    dbsession.flush()
    return cat


@pytest.fixture
def measure_type(dbsession, cat):
    from endi.models.accounting.base import (
        BaseAccountingMeasureType,
    )

    type_ = BaseAccountingMeasureType(
        order=1,
        category_id=cat.id,
        label="label",
        account_prefix="706",
    )
    dbsession.add(type_)
    dbsession.flush()
    return type_


class TestBaseAccountingMeasureTypeCategory:
    def get_them(self, dbsession):
        from endi.models.accounting.base import BaseAccountingMeasureTypeCategory

        cats = [
            BaseAccountingMeasureTypeCategory(label="label_%s" % i, order=i)
            for i in range(5)
        ]
        for cat in cats:
            dbsession.add(cat)
        dbsession.flush()
        return cats

    def test_move_up(self, dbsession):
        cats = self.get_them(dbsession)
        cats[2].move_up()
        assert cats[2].order == 1
        assert cats[1].order == 2

    def test_move_down(self, dbsession):
        cats = self.get_them(dbsession)
        cats[2].move_down()
        assert cats[2].order == 3
        assert cats[3].order == 2

    def test_get_categories(self, dbsession):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
        )

        cats = self.get_them(dbsession)
        assert BaseAccountingMeasureTypeCategory.get_categories() == cats

    def test_get_by_label(self, dbsession):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
        )

        cats = self.get_them(dbsession)
        assert BaseAccountingMeasureTypeCategory.get_by_label("label_2") == cats[2]
        assert BaseAccountingMeasureTypeCategory.get_by_label("wrong") is None

    def test_get_next_order(self, dbsession):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
        )

        assert BaseAccountingMeasureTypeCategory.get_next_order() == 0
        self.get_them(dbsession)
        assert BaseAccountingMeasureTypeCategory.get_next_order() == 5

    def test_insert(self, dbsession):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
        )

        cats = self.get_them(dbsession)
        BaseAccountingMeasureTypeCategory.insert(cats[2], 4)
        assert cats[2].order == 4
        assert cats[-1].order == 3

    def test_reorder(self, dbsession):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
        )

        cats = self.get_them(dbsession)

        cats[2].order = 15
        dbsession.merge(cats[2])
        BaseAccountingMeasureTypeCategory.reorder()
        assert cats[2].order == 4


class TestBaseAccountingMeasureType:
    def get_them(self, dbsession, cat):
        from endi.models.accounting.base import (
            BaseAccountingMeasureTypeCategory,
            BaseAccountingMeasureType,
        )

        cat2 = BaseAccountingMeasureTypeCategory(label="label_2", order=2)
        dbsession.add(cat2)
        dbsession.flush()

        types_ = [
            BaseAccountingMeasureType(order=i, label="label_%s" % i, category_id=cat.id)
            for i in range(5)
        ]
        types_[-1].category_id = cat2.id
        types_[-1].order = 1
        for type_ in types_:
            dbsession.add(type_)
        dbsession.flush()
        return types_

    def test_is_computed_total(self):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        type_ = BaseAccountingMeasureType(is_total=True, total_type="account_prefix")
        assert not type_.is_computed_total

        type_ = BaseAccountingMeasureType(is_total=True, total_type="complex_total")
        assert type_.is_computed_total

        type_ = BaseAccountingMeasureType(is_total=True, total_type="categories")
        assert type_.is_computed_total

    def test_match(self):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        type_ = BaseAccountingMeasureType(account_prefix="7,-766,654")
        assert type_.match("725")
        assert not type_.match("76666")
        assert not type_.match("1")
        assert type_.match("654")

    def test_move_up(self, dbsession, measure_type_category):
        types_ = self.get_them(dbsession, measure_type_category)
        types_[2].move_up()
        assert types_[2].order == 1
        assert types_[1].order == 2

    def test_move_down(self, dbsession, measure_type_category):
        types_ = self.get_them(dbsession, measure_type_category)
        types_[2].move_down()
        assert types_[2].order == 3
        assert types_[3].order == 2

    def test_compute_total(self, dbsession, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        type_ = BaseAccountingMeasureType(
            account_prefix="-100 / {Salaires (et Cotisations)}",
            is_total=True,
            total_type="complex_total",
        )
        # - 3.33333
        assert (
            3.34 + type_.compute_total({"Salaires (et Cotisations)": 30, "other": 2})
            < 0.01
        )

        assert type_.compute_total({"other": 2}) == 0
        assert type_.compute_total({"Salaires (et Cotisations)": 0}) == 0
        assert type_.compute_total({"Salaires (et Cotisations)": 2.5}) == -40
        assert type_.compute_total({"Salaires (et Cotisations)": 40}) == -2.5

        type_ = BaseAccountingMeasureType(
            account_prefix="-100 / {Salaires:Cotisations}",
            is_total=True,
            total_type="complex_total",
        )
        # Wrong syntax
        assert type_.compute_total({"Salaires:Cotisations": 15}) == 0

        type_ = BaseAccountingMeasureType(
            account_prefix="Achats,Produits,Salaires",
            is_total=True,
            total_type="categories",
        )
        assert (
            type_.compute_total({"Achats": 30.52, "Produits": 50, "other": 2.5})
            == 80.52
        )

    def test_get_categories(self, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        type_ = BaseAccountingMeasureType(account_prefix="Wrong,label_1")
        assert type_.get_categories() == [measure_type_category]

    def test_get_by_category(self, dbsession, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        self.get_them(dbsession, measure_type_category)
        assert (
            len(BaseAccountingMeasureType.get_by_category(measure_type_category.id))
            == 4
        )

    def test_get_next_order_by_category(self, dbsession, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        self.get_them(dbsession, measure_type_category)
        assert (
            BaseAccountingMeasureType.get_next_order_by_category(
                measure_type_category.id
            )
            == 4
        )

    def test_insert(self, dbsession, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        types_ = self.get_them(dbsession, measure_type_category)
        BaseAccountingMeasureType.insert(types_[0], 2)
        assert types_[1].order == 0
        assert types_[0].order == 2
        assert types_[2].order == 1

    def test_reorder(self, dbsession, measure_type_category):
        from endi.models.accounting.base import (
            BaseAccountingMeasureType,
        )

        types_ = self.get_them(dbsession, measure_type_category)
        types_[2].order = 18
        BaseAccountingMeasureType.reorder(measure_type_category.id)

        assert types_[2].order == 3
        assert types_[3].order == 2
        assert types_[-1].order == 1
