import pytest
import colander


@pytest.fixture
def mode(dbsession):
    from endi.models.payments import PaymentMode

    mode = PaymentMode(label="Chèque")
    dbsession.add(mode)
    dbsession.flush()
    return mode


@pytest.fixture
def bank(dbsession):
    from endi.models.payments import BankAccount

    bank = BankAccount(label="banque", code_journal="bq", compte_cg="123")
    dbsession.add(bank)
    dbsession.flush()
    return bank


def test_mode_validator(mode):
    from endi.forms.payments import deferred_payment_mode_validator

    c = colander.SchemaNode(colander.String())
    validator = deferred_payment_mode_validator(None, {})

    validator(c, mode.label)
    with pytest.raises(colander.Invalid):
        validator(c, "pièce en chocolat")


def test_bank_validator(bank):
    from endi.forms.payments import deferred_bank_account_validator

    c = colander.SchemaNode(colander.String())
    validator = deferred_bank_account_validator(None, {})
    validator(c, bank.id)
    with pytest.raises(colander.Invalid):
        validator(c, bank.id + 1)
