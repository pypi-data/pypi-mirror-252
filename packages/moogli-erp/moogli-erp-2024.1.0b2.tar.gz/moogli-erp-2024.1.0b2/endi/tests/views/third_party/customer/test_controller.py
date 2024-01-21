import colander

from endi.views.third_party.customer.controller import CustomerAddEditController
from endi.models.config import Config


class TestCustomerAddEditController:
    def test_get_customer_type_add(
        self,
        get_csrf_request_with_db,
        company,
    ):
        req = get_csrf_request_with_db(context=company)
        controller = CustomerAddEditController(req)

        for i in ("individual", "company", "internal"):
            assert controller.get_customer_type({"type": i}) == i
        Config.set("internal_invoicing_active", False)
        assert controller.get_customer_type({"type": "internal"}) == "company"

    def test_get_customer_type_edit(
        self,
        get_csrf_request_with_db,
        customer,
    ):
        request = get_csrf_request_with_db(context=customer)
        controller = CustomerAddEditController(request, edit=True)
        for typ in ("individual", "company", "internal"):
            customer.type = typ
            # Edit mode : type == le type du contexte
            assert controller.get_customer_type({"type": "company"}) == typ

    def test_schema(self, get_csrf_request_with_db, company):
        req = get_csrf_request_with_db(context=company)

        controller = CustomerAddEditController(req)
        submitted = {"type": "company"}
        schema = controller.get_schema(submitted)
        assert schema["company_name"].missing == colander.required

        # On recrée un controller parce que le schéma est en 'cache'
        controller = CustomerAddEditController(req)
        submitted = {"type": "individual"}
        schema = controller.get_schema(submitted)
        assert schema["lastname"].missing == colander.required
