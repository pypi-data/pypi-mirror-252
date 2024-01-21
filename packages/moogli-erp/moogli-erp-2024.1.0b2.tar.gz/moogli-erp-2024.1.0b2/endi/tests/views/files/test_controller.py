from io import BytesIO
import pytest
from endi.views.files.controller import FileController


@pytest.fixture
def ftypes(mk_business_type, mk_file_type):
    ftypes = {}
    for t in ("ftype1", "ftype2", "ftype3", "ftype4"):
        ftypes[t] = mk_file_type(label=t)
    return ftypes


@pytest.fixture
def btypes(mk_business_type):
    btypes = {}
    for b in ("default", "training"):
        btypes[b] = mk_business_type(b)
    return btypes


class TestFileController:
    @pytest.fixture
    def mk_invoice(
        self,
        get_csrf_request_with_db,
        dbsession,
        user,
        company,
        project,
        customer,
        business,
        mk_business_type_file_types,
        ftypes,
        btypes,
    ):
        from endi.models.task import Invoice

        request = get_csrf_request_with_db()

        def func(req_type="mandatory", validation=False, add_req=True, **kwargs):
            if add_req:
                mk_business_type_file_types(
                    ftypes["ftype1"], btypes["default"], "invoice", req_type, validation
                )
            if "project" not in kwargs:
                kwargs["project"] = project
            kwargs["user"] = user
            kwargs["company"] = company
            kwargs["business_type_id"] = btypes["default"].id
            kwargs["customer"] = customer
            node = Invoice.create(request, customer, kwargs)
            dbsession.flush()
            return node

        return func

    @pytest.fixture
    def mk_controller(self, get_csrf_request_with_db, mk_invoice):
        def factory(context=None):
            if context is None:
                context = mk_invoice()
            request = get_csrf_request_with_db(context=context)
            controller = FileController(request)
            return controller

        return factory

    @pytest.fixture
    def controller(self, mk_controller):
        return mk_controller()

    def test_get_schema(self, controller):
        for key in (
            "come_from",
            "popup",
            "upload",
            "description",
            "file_type_id",
            "indicator_id",
        ):
            assert key in controller.get_schema()

    def test_file_to_appstruct(self, config, controller, mk_file):
        config.add_route("/files/{id}", "/files/{id}")
        f = mk_file()
        assert controller.file_to_appstruct(f) == {
            "name": f.name,
            "description": f.description,
            "file_type_id": f.file_type_id,
            "upload": {
                "filename": f.name,
                "uid": str(f.id),
                "preview_url": f"/files/{f.id}?action=download",
            },
        }

    def test_add_file_to_node(self, controller, ftypes):
        ftype = list(ftypes.values())[0]
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": ftype.id,
        }
        res = controller._add(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == controller.request.context

    def test_add_file_to_task_with_indicator_business_mandatory(
        self,
        mk_controller,
        mk_invoice,
    ):
        context = mk_invoice(req_type="business_mandatory")
        controller = mk_controller(context)
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": context.business.file_requirements[0].file_type_id,
            "indicator_id": context.business.file_requirements[0].id,
            "node_id": context.id,
        }
        res = controller._add(attributes, context)
        assert res.parent == context.business

    def test_add_file_to_task_with_file_type_matching_business_mandatory(
        self,
        mk_controller,
        mk_invoice,
    ):
        context = mk_invoice(req_type="business_mandatory")
        controller = mk_controller(context)
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": context.business.file_requirements[0].file_type_id,
        }
        res = controller._add(attributes, context)
        assert res.parent == context.business

    def test_add_file_to_task_with_indicator_project_mandatory(
        self,
        mk_controller,
        mk_invoice,
    ):
        context = mk_invoice(req_type="project_mandatory")
        controller = mk_controller(context)
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": context.project.file_requirements[0].file_type_id,
            "indicator_id": context.project.file_requirements[0].id,
        }
        res = controller._add(attributes, context)

        assert res.parent == context.project

    def test_add_file_to_task_with_file_type_matching_project_mandatory(
        self,
        mk_controller,
        mk_invoice,
    ):
        context = mk_invoice(req_type="project_mandatory")
        controller = mk_controller(context)
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": context.project.file_requirements[0].file_type_id,
        }
        res = controller._add(attributes, context)

        assert res.parent == context.project

    def test_add_file_to_business_with_indicator_project_mandatory(
        self,
        mk_controller,
        mk_invoice,
    ):
        invoice = mk_invoice(req_type="project_mandatory")
        controller = mk_controller(invoice.business)
        f = BytesIO(b"test")
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": f,
            },
            "description": "test",
            "file_type_id": invoice.project.file_requirements[0].file_type_id,
            "indicator_id": invoice.project.file_requirements[0].id,
        }
        res = controller._add(attributes)

        assert res.parent == invoice.project

    def test_edit_file(self, mk_controller, mk_file, mk_invoice, ftypes):
        ftype = list(ftypes.values())[0]
        inv = mk_invoice()
        f = mk_file(parent=inv)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": ftype.id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == f.parent

    def test_edit_file_to_task_with_indicator_business_mandatory(
        self, mk_controller, mk_file, mk_invoice, ftypes
    ):
        ftype = list(ftypes.values())[0]
        inv = mk_invoice(req_type="business_mandatory")
        f = mk_file(parent=inv)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": inv.business.file_requirements[0].file_type_id,
            "indicator_id": inv.business.file_requirements[0].id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == inv.business

    def test_edit_file_to_task_with_file_type_matching_business_mandatory(
        self, mk_controller, mk_file, mk_invoice, ftypes
    ):
        ftype = list(ftypes.values())[0]
        inv = mk_invoice(req_type="business_mandatory")
        f = mk_file(parent=inv)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": inv.business.file_requirements[0].file_type_id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == inv.business

    def test_edit_file_to_task_with_indicator_project_mandatory(
        self, mk_controller, mk_file, mk_invoice, ftypes
    ):
        ftype = list(ftypes.values())[0]
        inv = mk_invoice(req_type="project_mandatory")
        f = mk_file(parent=inv)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": inv.project.file_requirements[0].file_type_id,
            "indicator_id": inv.project.file_requirements[0].id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == inv.project

    def test_edit_file_to_task_with_file_type_project_mandatory(
        self, mk_controller, mk_file, mk_invoice, ftypes
    ):
        ftype = list(ftypes.values())[0]
        inv = mk_invoice(req_type="project_mandatory")
        f = mk_file(parent=inv)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": inv.project.file_requirements[0].file_type_id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.name == "test.pdf"
        assert res.description == "test"
        assert res.file_type_id == ftype.id
        assert res.parent == inv.project

    def test_edit_file_with_different_parent_id(
        self, mk_controller, mk_file, ftypes, mk_invoice
    ):
        ftype = list(ftypes.values())[0]
        source_invoice = mk_invoice()
        dest_invoice = mk_invoice(add_req=False)

        f = mk_file(parent=source_invoice)
        attributes = {
            "upload": {
                "size": 1520,
                "mimetype": "application/pdf",
                "filename": "test.pdf",
                "fp": BytesIO(b"test"),
            },
            "description": "test",
            "file_type_id": ftype.id,
            "parent_id": dest_invoice.id,
        }
        controller = mk_controller(context=f)
        res = controller._edit(attributes)
        assert res.parent == dest_invoice
