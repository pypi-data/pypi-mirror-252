import pytest
import colander


from endi.models.task import Task, Estimation
from endi.forms.tasks.task import (
    get_add_edit_taskline_schema,
    get_add_edit_tasklinegroup_schema,
    get_add_edit_discountline_schema,
    get_edit_task_schema,
    get_add_task_schema,
)


def test_task_line_description():
    schema = get_add_edit_taskline_schema(includes=("description",))
    schema = schema.bind()
    value = {"description": "test\n"}
    assert schema.deserialize(value) == {"description": "test"}
    value = {"description": "\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_cost():
    schema = get_add_edit_taskline_schema(includes=("cost",))
    schema = schema.bind()
    value = {"cost": 12.50}
    assert schema.deserialize(value) == {"cost": 1250000}
    value = {"cost": "a"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_quantity():
    schema = get_add_edit_taskline_schema(includes=("quantity",))
    schema = schema.bind()
    value = {"quantity": 1}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_unity(unity):
    schema = get_add_edit_taskline_schema(includes=("unity",))
    schema = schema.bind()
    value = {"unity": "h"}
    assert schema.deserialize(value) == value
    value = {"unity": "Panies"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    schema.deserialize(value)


def test_task_line_tva(tva):
    schema = get_add_edit_taskline_schema(includes=("tva",))
    schema = schema.bind()
    value = {"tva": 20.00}
    assert schema.deserialize(value) == {"tva": 2000}
    value = {"tva": 21.00}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_product_id(config, request_with_config, estimation, product):
    schema = get_add_edit_taskline_schema(includes=("product_id",))
    request_with_config.context = estimation
    schema = schema.bind(request=request_with_config)
    value = {"product_id": product.id}
    assert schema.deserialize(value) == value
    value = {"product_id": product.id + 1}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    assert schema.deserialize(value) == value


def test_task_line(
    config, request_with_config, estimation, unity, tva, product, product_without_tva
):
    schema = get_add_edit_taskline_schema()
    request_with_config.context = estimation
    schema = schema.bind(request=request_with_config)
    value = {
        "description": "test",
        "cost": 450,
        "date": colander.null,
        "quantity": 1,
        "unity": "h",
        "tva": 20.00,
        "product_id": product.id,
    }
    assert schema.deserialize(value) == {
        "description": "test",
        "cost": 45000000,
        "date": colander.null,
        "mode": "ht",
        "quantity": 1.0,
        "unity": "h",
        "tva": 2000,
        "product_id": product.id,
        "order": 1,
    }
    value = {
        "description": "test",
        "cost": 450,
        "date": colander.null,
        "quantity": 1,
        "unity": "h",
        "tva": 20.00,
        "product_id": product_without_tva.id,
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_group_lines(tva, unity):
    schema = get_add_edit_tasklinegroup_schema(includes=("lines",))
    schema = schema.bind()
    value = {"lines": []}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)

    value = {
        "lines": [
            {
                "cost": 15,
                "date": colander.null,
                "tva": 20,
                "description": "description",
                "unity": "h",
                "quantity": 5,
            }
        ]
    }
    assert schema.deserialize(value) == {
        "lines": [
            {
                "cost": 1500000,
                "date": colander.null,
                "tva": 2000,
                "description": "description",
                "mode": "ht",
                "unity": "h",
                "quantity": 5.0,
                "order": 1,
            }
        ]
    }


def test_task_line_group_task_id():
    schema = get_add_edit_tasklinegroup_schema(includes=("task_id",))
    value = {"task_id": 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_group(unity, tva):
    schema = get_add_edit_tasklinegroup_schema()
    schema = schema.bind()
    value = {
        "task_id": 5,
        "title": "title",
        "description": "description",
        "order": 5,
        "lines": [
            {
                "cost": 15,
                "tva": 20,
                "description": "description",
                "unity": "h",
                "quantity": 5,
                "order": 2,
            }
        ],
    }
    expected_value = {
        "task_id": 5,
        "title": "title",
        "description": "description",
        "order": 5,
        "display_details": True,
        "lines": [
            {
                "cost": 1500000,
                "date": colander.null,
                "tva": 2000,
                "description": "description",
                "mode": "ht",
                "unity": "h",
                "quantity": 5.0,
                "order": 2,
            }
        ],
    }
    assert schema.deserialize(value) == expected_value


def test_discount_line_description():
    schema = get_add_edit_discountline_schema(includes=("description",))
    value = {"description": "description"}
    assert schema.deserialize(value) == value
    value = {"description": "<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_amount():
    schema = get_add_edit_discountline_schema(includes=("amount",))
    schema = schema.bind()
    value = {"amount": 12.50}
    assert schema.deserialize(value) == {"amount": 1250000}
    value = {"amount": "a"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_tva(tva):
    schema = get_add_edit_discountline_schema(includes=("tva",))
    schema = schema.bind()
    value = {"tva": 20.00}
    assert schema.deserialize(value) == {"tva": 2000}
    value = {"tva": 21.00}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line_task_id():
    schema = get_add_edit_discountline_schema(includes=("task_id",))
    schema = schema.bind()
    value = {"task_id": 5}
    assert schema.deserialize(value) == value
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_discount_line(tva):
    schema = get_add_edit_discountline_schema()
    schema = schema.bind()
    value = {"task_id": 5, "description": "description", "amount": 5, "tva": 20.0}
    assert schema.deserialize(value) == {
        "task_id": 5,
        "description": "description",
        "amount": 500000,
        "tva": 2000,
    }


def test_task_description():
    schema = get_edit_task_schema(Task, includes=("description",))
    schema = schema.bind()
    value = {"description": "description"}
    assert schema.deserialize(value) == value
    value = {"description": "<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_address():
    schema = get_edit_task_schema(Task, includes=("address",))
    schema = schema.bind()
    value = {"address": "address"}
    assert schema.deserialize(value) == value
    value = {"address": "<br /><p></p>\n"}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_mentions(mention):
    schema = get_edit_task_schema(Task, includes=("mentions",))
    schema = schema.bind()
    value = {"mentions": [mention.id]}
    assert schema.deserialize(value) == value
    value = {"mentions": [mention.id + 1]}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_date():
    import datetime

    schema = get_edit_task_schema(Task, includes=("date",))
    schema = schema.bind()
    value = {"date": datetime.date.today().isoformat()}
    assert schema.deserialize(value) == {"date": datetime.date.today()}
    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_line_groups(tva, unity):
    schema = get_edit_task_schema(Task, includes=("line_groups",))
    schema = schema.bind()
    value = {"line_groups": []}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)
    value = {
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "lines": [
                    {
                        "cost": 15,
                        "date": colander.null,
                        "tva": 20,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5,
                        "order": 2,
                    }
                ],
            }
        ]
    }
    expected_value = {
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "display_details": True,
                "lines": [
                    {
                        "cost": 1500000,
                        "date": colander.null,
                        "tva": 2000,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ],
            }
        ]
    }
    assert schema.deserialize(value) == expected_value


def test_task_payment_conditions():
    schema = get_edit_task_schema(Task, includes=("payment_conditions",))
    schema = schema.bind()

    value = {"payment_conditions": "À réception de facture"}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_task_isadmin():
    schema = get_edit_task_schema(Task, isadmin=False)
    assert "status" not in schema
    schema = get_edit_task_schema(Task, isadmin=True)
    assert "status" in schema


def test_task(tva, unity, request_with_config):
    import datetime

    schema = get_edit_task_schema(Task)
    schema = schema.bind(request=request_with_config)
    value = {
        "name": "Test task",
        "date": datetime.date.today().isoformat(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "status_comment": "Test comment",
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "lines": [
                    {
                        "cost": 15,
                        "date": colander.null,
                        "tva": 20,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    expected_value = {
        "name": "Test task",
        "date": datetime.date.today(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "status_comment": "Test comment",
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "display_details": True,
                "lines": [
                    {
                        "cost": 1500000,
                        "date": colander.null,
                        "tva": 2000,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in list(expected_value.items()):
        assert result[key] == value


CUSTOM_FIELDS = (
    "workplace",
    "insurance_id",
    "start_date",
    "end_date",
    "first_visit",
)


def test_task_custom_fields_not_present(tva, unity, request_with_config):
    schema = get_edit_task_schema(Task)
    schema = schema.bind(request=request_with_config)

    for field in CUSTOM_FIELDS:
        assert field not in schema


def test_task_custom_fields_required(
    tva, unity, request_with_config, mk_form_field_definition
):
    for field in CUSTOM_FIELDS:
        mk_form_field_definition(title=field, field_name=field, required=True)
    schema = get_edit_task_schema(Task)
    schema = schema.bind(request=request_with_config)
    for field in CUSTOM_FIELDS:
        assert field in schema
        assert schema[field].title == field
        assert schema[field].missing == colander.required


def test_task_custom_fields_not_required(
    tva, unity, request_with_config, mk_form_field_definition
):
    for field in CUSTOM_FIELDS:
        mk_form_field_definition(title=field, field_name=field, required=False)
    schema = get_edit_task_schema(Task)
    schema = schema.bind(request=request_with_config)
    for field in CUSTOM_FIELDS:
        assert field in schema
        assert schema[field].title == field
        assert schema[field].missing is None


def test_task_custom_fields_not_visible(
    tva, unity, request_with_config, mk_form_field_definition
):
    for field in CUSTOM_FIELDS:
        mk_form_field_definition(
            title=field, field_name=field, required=False, visible=False
        )
    schema = get_edit_task_schema(Task)
    schema = schema.bind(request=request_with_config)
    for field in CUSTOM_FIELDS:
        assert field not in schema


def test_not_task_id_ref_bug_822():
    from endi.models.task import Estimation

    schema = get_edit_task_schema(Estimation)
    assert "id" not in schema
    schema = get_edit_task_schema(Estimation, includes=("id",))
    assert "id" not in schema


class TestAddTaskSchema:
    @pytest.fixture
    def _schema_factory(self, get_csrf_request_with_db, company):
        def factory(_company=company):
            request = get_csrf_request_with_db()
            schema = get_add_task_schema(Estimation, request, _company.id)
            schema = schema.bind(request=request)
            return schema

        return factory

    def test_create_schema(
        self, _schema_factory, project, customer, default_business_type
    ):
        _schema = _schema_factory()
        create_dict = {
            "name": "test devis",
            "project_id": str(project.id),
            "customer_id": str(customer.id),
            "business_type_id": str(default_business_type.id),
        }
        result = _schema.deserialize(create_dict)
        assert result["project_id"] == project.id
        assert result["customer_id"] == customer.id

    def test_create_required(
        self, _schema_factory, project, customer, default_business_type
    ):
        schema = _schema_factory()
        create_dict = {
            "name": "test devis",
            "project_id": str(project.id),
            "customer_id": str(customer.id),
            "business_type_id": str(default_business_type.id),
        }
        for key in "name", "customer_id", "project_id":
            wrong = create_dict.copy()
            wrong.pop(key)
            with pytest.raises(colander.Invalid):
                schema.deserialize(wrong)

    def test_bad_company(
        self, _schema_factory, project, customer, default_business_type, company2
    ):
        schema = _schema_factory(company2)
        create_dict = {
            "name": "test devis",
            "project_id": str(project.id),
            "customer_id": str(customer.id),
            "business_type_id": str(default_business_type.id),
        }
        with pytest.raises(colander.Invalid):
            schema.deserialize(create_dict)

    def test_wrong_customer_project_pair(
        self,
        _schema_factory,
        customer,
        project,  # On veut au moins un projet pour le customer
        default_business_type,
        mk_customer,
        mk_project,
    ):
        # Client et mauvais projet  : ERROR
        customer2 = mk_customer()
        project2 = mk_project(customers=[customer2])
        schema = _schema_factory()
        create_dict = {
            "name": "test devis",
            "project_id": str(project2.id),
            "customer_id": str(customer.id),
            "business_type_id": str(default_business_type.id),
        }
        with pytest.raises(colander.Invalid):
            schema.deserialize(create_dict)

    def test_attach_customer_project(
        self,
        _schema_factory,
        customer,  # on veut au moins un customer dans le projet
        project,
        default_business_type,
        mk_customer,
    ):
        # Ref #3609
        # Client sans projet (OK)
        customer2 = mk_customer()
        schema = _schema_factory()
        create_dict = {
            "name": "test devis",
            "project_id": str(project.id),
            "customer_id": str(customer2.id),
            "business_type_id": str(default_business_type.id),
        }
        result = schema.deserialize(create_dict)
        assert result["customer_id"] == customer2.id
        assert result["project_id"] == project.id
