import colander
import pytest
import datetime
from endi.forms.tasks.payment import PaymentSchema
from endi.forms.tasks.payment import get_payment_schema


NOW = datetime.date.today()


class TestPaymentSchema:
    def get_schema_node(self, request, node):
        schema = get_payment_schema().bind(request=request)
        return schema[node]

    def test_paymentform_schema(
        self,
        get_csrf_request_with_db,
        populated_invoice,
        mode,
        bank,
        customer_bank,
        user,
        customer,
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = get_payment_schema().bind(request=request)

        value = {
            "bank_remittance_id": "Remittance",
            "amount": "12.53",
            "date": "2015-08-07",
            "bank_id": str(bank.id),
            "customer_bank_id": str(customer_bank.id),
            "check_number": "0123456789",
            "mode": mode.label,
            "resulted": True,
            "issuer": customer.label,
        }
        expected_value = {
            "come_from": "",
            "bank_remittance_id": "Remittance",
            "amount": 1253000,
            "date": datetime.date(2015, 8, 7),
            "bank_id": bank.id,
            "customer_bank_id": customer_bank.id,
            "check_number": "0123456789",
            "mode": mode.label,
            "resulted": True,
            "issuer": customer.label,
        }
        assert schema.deserialize(value) == expected_value

    def test_deferred_total_validator(
        self,
        get_csrf_request_with_db,
        populated_invoice,
        mode,
        bank,
        customer_bank,
        user,
    ):
        request = get_csrf_request_with_db(user=user, context=populated_invoice)
        schema = PaymentSchema().bind(request=request)

        amount_node = schema["amount"]
        # paiement complet
        assert amount_node.deserialize("150.0") == 15000000
        # Aved un peu plus
        assert amount_node.deserialize("155.0") == 15500000
        # Paiement partiel
        assert amount_node.deserialize("120.0") == 12000000

        # Paiement trop gros
        with pytest.raises(colander.Invalid):
            amount_node.deserialize("155.1")

        # Paiement inférieur à 0
        with pytest.raises(colander.Invalid):
            amount_node.deserialize("-1")

    def test_deferred_negative_total_validator(
        self,
        get_csrf_request_with_db,
        mk_invoice,
        mode,
        bank,
        customer_bank,
        mk_task_line,
        mk_task_line_group,
        user,
    ):
        populated_invoice = mk_invoice(name="negative populated_invoice")
        task_line_group = mk_task_line_group()
        # 150€ TTC
        task_line = mk_task_line(cost=-12500000, group=task_line_group)
        populated_invoice.line_groups = [task_line_group]
        task_line_group.lines = [task_line]
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = PaymentSchema().bind(request=request)
        amount_node = schema["amount"]
        assert amount_node.deserialize("-150.0") == -15000000
        assert amount_node.deserialize("-130.0") == -13000000

        with pytest.raises(colander.Invalid):
            amount_node.deserialize("-160.0")
        with pytest.raises(colander.Invalid):
            amount_node.deserialize("1")

    def test_payment_mode(
        self, get_csrf_request_with_db, populated_invoice, mode, user
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "mode")

        value = mode.label
        assert schema.deserialize(value) == value

        value = "error"
        with pytest.raises(colander.Invalid):
            schema.deserialize(value)

        value = {}
        with pytest.raises(colander.Invalid):
            schema.deserialize(value)

    def test_payment_bank_remittance_id(
        self, get_csrf_request_with_db, populated_invoice, user
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "bank_remittance_id")

        value = "test"
        assert schema.deserialize(value) == value

    def test_payment_date(self, get_csrf_request_with_db, populated_invoice, user):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "date")
        value = NOW.isoformat()
        assert schema.deserialize(value) == NOW
        value = ""
        with pytest.raises(colander.Invalid):
            schema.deserialize(value)

    def test_payment_bank_id(
        self, get_csrf_request_with_db, populated_invoice, user, bank
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "bank_id")

        value = bank.id
        assert schema.deserialize(value) == value

        value = bank.id + 1
        with pytest.raises(colander.Invalid):
            schema.deserialize(value)

    def test_payment_customer_bank_id(
        self, get_csrf_request_with_db, populated_invoice, user, customer_bank
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "customer_bank_id")

        value = customer_bank.id
        assert schema.deserialize(value) == value
        value = ""
        assert schema.deserialize(value) is colander.drop

        value = customer_bank.id + 1
        with pytest.raises(colander.Invalid):
            schema.deserialize(value)

    def test_payment_check_number(
        self, get_csrf_request_with_db, populated_invoice, user
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "check_number")

        value = "0123456789"
        assert schema.deserialize(value) == value

    def test_payment_issuer(
        self, get_csrf_request_with_db, populated_invoice, user, customer
    ):
        request = get_csrf_request_with_db(context=populated_invoice, user=user)
        schema = self.get_schema_node(request, "issuer")

        value = customer.label
        assert schema.deserialize(value) == value
