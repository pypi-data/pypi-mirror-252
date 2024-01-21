from unittest.mock import MagicMock
from endi.forms.project import customer_dictify


def test_customer_dictify():
    customer = MagicMock(id=12)
    # deform is expecting a string (while it's an integer type
    assert customer_dictify(customer) == 12
