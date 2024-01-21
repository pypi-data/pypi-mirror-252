import pytest
from endi.tests.tools import Dummy


@pytest.fixture
def dummyttc():
    return Dummy(mode="ttc", internal=False)


def test_duplicate_task_line(task_line):
    newline = task_line.duplicate()
    for i in ("order", "cost", "tva", "description", "quantity", "unity", "product_id"):
        assert getattr(newline, i) == getattr(task_line, i)


def test_duplicate_mode_ht_task_line(task_line):
    newline = task_line.duplicate()
    assert newline.mode == task_line.mode
    assert newline.mode == "ht"


def test_duplicate_mode_ttc_task_line(task_line):
    task_line.mode = "ttc"
    newline = task_line.duplicate()
    assert newline.mode == task_line.mode
    assert newline.mode == "ttc"


def test_gen_cancelinvoiceline(task_line):
    newline = task_line.gen_cancelinvoice_line()
    for i in ("order", "tva", "description", "quantity", "unity", "product_id"):
        assert getattr(newline, i) == getattr(task_line, i)
    assert newline.cost == -1 * task_line.cost


def test_gen_cancelinvoiceline_ht_mode(task_line):
    newline = task_line.gen_cancelinvoice_line()
    assert newline.mode == task_line.mode
    assert newline.mode == "ht"


def test_gen_cancelinvoiceline_ttc_mode(task_line):
    task_line.mode = "ttc"
    newline = task_line.gen_cancelinvoice_line()
    assert newline.mode == task_line.mode
    assert newline.mode == "ttc"


def test_duplicate_task_line_group(
    task_line_group, task_line, invoice_one, invoice_two
):
    task_line_group.lines = [task_line]
    invoice_one.line_groups = [task_line_group]
    newgroup = invoice_one.line_groups[0].duplicate()
    invoice_one.line_groups.append(newgroup)
    for i in ("order", "description", "title"):
        assert getattr(invoice_one.line_groups[0], i) == getattr(
            invoice_one.line_groups[1], i
        )

    assert (
        invoice_one.line_groups[0].total_ht() == invoice_one.line_groups[1].total_ht()
    )


def test_task_line_from_sale_product(sale_product, dummyttc):
    from endi.models.task.task import TaskLine

    t = TaskLine.from_sale_product(sale_product)
    assert t.tva == sale_product.tva.value
    assert t.cost == sale_product.ht
    assert t.mode == "ht"
    assert t.description == sale_product.description
    assert t.unity == sale_product.unity
    assert t.product_id == sale_product.product_id

    t = TaskLine.from_sale_product(sale_product, document=dummyttc)
    assert t.cost == sale_product.ttc
    assert t.mode == "ttc"


def test_task_line_group_from_sale_product_work(
    sale_product_work,
    mk_sale_product_work_item,
    tva,
    product,
    dummyttc,
):
    item = mk_sale_product_work_item(
        _supplier_ht=2,
        _mode="supplier_ht",
        _unity="feuille",
        sale_product_work_id=sale_product_work.id,
    )
    item.sync_amounts()

    from endi.models.task.task import TaskLineGroup

    t = TaskLineGroup.from_sale_product_work(sale_product_work)
    assert len(t.lines) == 1
    line = t.lines[0]
    assert line.tva == tva.value
    assert line.cost == item.ht
    assert line.description == item.description
    assert line.unity == item.unity

    assert line.quantity == item.quantity
    assert line.total_ht() == item.total_ht

    t = TaskLineGroup.from_sale_product_work(sale_product_work, document=dummyttc)
    line = t.lines[0]
    assert line.cost == item.total_ttc()
    assert line.mode == "ttc"
