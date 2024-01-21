import pytest
from endi.tests.tools import Dummy
from endi.models.services.sale_file_requirements import (
    SaleFileRequirementService,
    TaskFileRequirementService,
    BusinessFileRequirementService,
)


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


@pytest.fixture
def file_instance(dbsession, ftypes):
    from endi.models.files import File

    node = File(
        name="file01",
        file_type_id=ftypes["ftype1"].id,
        size=13,
        mimetype="text",
    )
    node.data = b"test content"
    dbsession.add(node)
    dbsession.flush()
    return node


@pytest.fixture
def mk_invoice(
    get_csrf_request_with_db,
    user,
    company,
    project,
    customer,
    mk_business_type_file_types,
    ftypes,
    btypes,
):
    request = get_csrf_request_with_db()
    from endi.models.task import Invoice

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
        request.dbsession.add(node)
        request.dbsession.flush()
        return node

    return func


@pytest.fixture
def mk_estimation(
    get_csrf_request_with_db,
    user,
    company,
    project,
    customer,
    mk_business_type_file_types,
    ftypes,
    btypes,
):
    request = get_csrf_request_with_db()
    from endi.models.task import Estimation

    def func(req_type="mandatory", validation=False, add_req=True, **kwargs):
        if add_req:
            # Ajout d'un fichier requis niveau affaire
            mk_business_type_file_types(
                ftypes["ftype1"], btypes["default"], "estimation", req_type, validation
            )
        if "project" not in kwargs:
            kwargs["project"] = project
        kwargs["user"] = user
        kwargs["company"] = company
        kwargs["business_type_id"] = btypes["default"].id
        node = Estimation.create(request, customer, kwargs)
        request.dbsession.add(node)
        request.dbsession.flush()
        return node

    return func


@pytest.fixture
def mk_business(
    dbsession,
    mk_business_type_file_types,
    ftypes,
    btypes,
    project,
):
    from endi.models.project.business import Business

    def func(
        req_type="mandatory",
        validation=False,
        tasks=[],
        project=project,
        btype="default",
    ):
        business_node = Business.create(
            name="business",
            project=project,
            business_type_id=btypes[btype].id,
        )
        business_node.tasks = tasks
        mk_business_type_file_types(
            ftypes["ftype1"], btypes["default"], "business", req_type, validation
        )
        dbsession.add(business_node)
        dbsession.flush()
        SaleFileRequirementService.populate(business_node)
        return business_node

    return func


@pytest.fixture
def project_with_file(project, file_instance):
    project.files = [file_instance]
    return project


class TestPopulate:
    @staticmethod
    def test_base_populate(mk_invoice, ftypes):
        node = mk_invoice()
        assert len(node.file_requirements) == 1
        assert node.file_requirements[0].requirement_type == "mandatory"
        assert node.file_requirements[0].file_type_id == ftypes["ftype1"].id
        assert node.file_requirements[0].status == "danger"
        assert node.file_requirements[0].validation_status == "valid"

    @staticmethod
    def test_populate_recommended(mk_invoice):
        node = mk_invoice("recommended")
        assert node.file_requirements[0].requirement_type == "recommended"
        assert node.file_requirements[0].status == "warning"
        assert node.file_requirements[0].validation_status == "valid"

    @staticmethod
    def test_populate_validation(mk_invoice):
        node = mk_invoice(validation=True)
        assert node.file_requirements[0].status == "danger"
        assert node.file_requirements[0].validation_status == "none"

    @staticmethod
    def test_populate_business_mandatory(mk_invoice):
        node = mk_invoice("business_mandatory")
        assert (
            node.business.file_requirements[0].requirement_type == "business_mandatory"
        )
        assert node.business.file_requirements[0].doctype == "invoice"

    @staticmethod
    def test_populate_project_mandatory(mk_invoice, project):
        mk_invoice("project_mandatory")
        assert project.file_requirements[0].requirement_type == "project_mandatory"
        assert project.file_requirements[0].doctype == "invoice"

    @staticmethod
    def test_populate_void(mk_business_type_file_types, ftypes, btypes):
        mk_business_type_file_types(
            ftypes["ftype1"], btypes["default"], "invoice", "recommended"
        )
        node = Dummy(
            file_requirements=[],
            type_="estimation",
            business_type_id=btypes["default"].id,
        )
        SaleFileRequirementService.populate(node)
        assert len(node.file_requirements) == 0


class TestCollectIndicators:
    @staticmethod
    def test_get_related_project_indicators(mk_invoice):
        node = mk_invoice("project_mandatory")
        indicators = SaleFileRequirementService._get_related_project_indicators(node)
        assert len(indicators) == 1

    @staticmethod
    def test_get_related_business_indicators(mk_invoice):
        node = mk_invoice("business_mandatory")
        indicators = TaskFileRequirementService._get_related_business_indicators(node)
        assert len(indicators) == 1

    @staticmethod
    def test_get_attached_indicators_mandatory(mk_invoice, ftypes):
        invoice = mk_invoice("mandatory")

        result = TaskFileRequirementService.get_attached_indicators(
            invoice, ftypes["ftype1"].id
        )
        assert len(result) == 1

    @staticmethod
    def test_get_attached_indicators_recommended(mk_invoice, ftypes):
        invoice = mk_invoice("recommended")

        result = TaskFileRequirementService.get_attached_indicators(
            invoice, ftypes["ftype1"].id
        )
        assert len(result) == 1

    @staticmethod
    def test_get_business_mandatory_indicators_from_task(mk_invoice):
        invoice1 = mk_invoice("business_mandatory")

        result = BusinessFileRequirementService.get_attached_indicators(
            invoice1.business
        )
        assert len(result) == 1

    @staticmethod
    def test_get_direct_business_mandatory_indicators(mk_invoice, mk_business, ftypes):
        invoice1 = mk_invoice("mandatory")
        business = mk_business("business_mandatory", tasks=[invoice1])

        result = BusinessFileRequirementService.get_attached_indicators(
            business, ftypes["ftype1"].id
        )
        assert len(result) == 1

    @staticmethod
    def test_get_business_mandatory_indicators_bug_1853(
        mk_estimation,
        ftypes,
        dbsession,
    ):
        estimation = mk_estimation("business_mandatory")
        estimation2 = mk_estimation("business_mandatory", add_req=False)

        result = TaskFileRequirementService._get_related_business_indicators(
            estimation, ftypes["ftype1"].id
        )
        assert len(result) == 0
        result = TaskFileRequirementService._get_related_business_indicators(
            estimation2, ftypes["ftype1"].id
        )
        assert len(result) == 0

    @staticmethod
    def test_get_related_project_indicators_from_task(
        mk_invoice, mk_business, ftypes, project
    ):
        invoice = mk_invoice("project_mandatory", project=project)
        result = TaskFileRequirementService._get_related_project_indicators(
            invoice, ftypes["ftype1"].id
        )
        assert len(result) == 1

    @staticmethod
    def test_get_related_project_indicators_from_business(mk_business, ftypes, project):
        business = mk_business("project_mandatory", project=project)
        result = BusinessFileRequirementService._get_related_project_indicators(
            business, ftypes["ftype1"].id
        )
        assert len(result) == 1
        result = BusinessFileRequirementService._get_related_project_indicators(
            business
        )
        assert len(result) == 1

    @staticmethod
    def test_get_file_related_indicators(
        dbsession, mk_invoice, mk_business, file_instance
    ):
        invoice = mk_invoice("mandatory")
        invoice.file_requirements[0].file_id = file_instance.id
        dbsession.merge(invoice.file_requirements[0])
        business = mk_business()
        business.file_requirements[0].file_id = file_instance.id
        dbsession.merge(business.file_requirements[0])

        res = SaleFileRequirementService.get_file_related_indicators(file_instance.id)
        dbsession.delete(file_instance)
        assert len(res) == 2


class TestIndicatorCheck:
    @staticmethod
    def test_check_files_no_ok(mk_invoice):
        invoice = mk_invoice("business_mandatory")
        req = BusinessFileRequirementService.get_attached_indicators(invoice.business)[
            0
        ]
        assert req.status == "danger"

    @staticmethod
    def test_check_files_ok(mk_invoice, file_instance):
        invoice = mk_invoice("business_mandatory")

        req = BusinessFileRequirementService.get_attached_indicators(invoice.business)[
            0
        ]
        req.set_file(file_instance.id)
        assert req.status == "success"
        assert req.file_id == file_instance.id

    @staticmethod
    def test_business_indicator_update_on_invoice_create(
        dbsession, mk_invoice, mk_business, ftypes
    ):
        business = mk_business()
        assert BusinessFileRequirementService.get_status(business) == "danger"
        req = BusinessFileRequirementService.get_attached_indicators(business)[0]
        req.status = "success"
        dbsession.merge(req)
        dbsession.flush()
        assert BusinessFileRequirementService.get_status(business) == "success"

        mk_invoice("business_mandatory", business=business)
        assert BusinessFileRequirementService.get_status(business) == "danger"
