import pytest

pytest.mark.usefixtures("config")


@pytest.fixture
def file_type(dbsession):
    from endi.models.files import FileType

    f = FileType(label="Label")
    dbsession.add(f)
    dbsession.flush()
    return f


def test_file_type_add(config, get_csrf_request_with_db, dbsession):
    from endi.views.admin.main.file_types import (
        FileTypeAddView,
        FILE_TYPE_ROUTE,
    )
    from endi.models.files import FileType

    config.add_route(FILE_TYPE_ROUTE, FILE_TYPE_ROUTE)
    appstruct = {
        "label": "Label",
    }
    view = FileTypeAddView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    element = FileType.get_by_label("Label")
    assert element is not None


def test_file_type_edit(config, get_csrf_request_with_db, dbsession, file_type):
    from endi.views.admin.main.file_types import (
        FileTypeEditView,
        FILE_TYPE_ROUTE,
    )

    appstruct = {
        "label": "New label",
    }
    config.add_route(FILE_TYPE_ROUTE, FILE_TYPE_ROUTE)
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeEditView(req)
    view.submit_success(appstruct)
    assert req.context.label == "New label"


def test_file_type_disable(config, get_csrf_request_with_db, dbsession, file_type):
    from endi.views.admin.main.file_types import (
        FileTypeDisableView,
        FILE_TYPE_ROUTE,
    )

    config.add_route(FILE_TYPE_ROUTE, FILE_TYPE_ROUTE)
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeDisableView(req)
    view()
    assert not file_type.active


def test_file_type_delete(config, get_csrf_request_with_db, dbsession, file_type):
    from endi.views.admin.main.file_types import (
        FileTypeDeleteView,
        FILE_TYPE_ROUTE,
    )
    from endi.models.files import FileType

    config.add_route(FILE_TYPE_ROUTE, FILE_TYPE_ROUTE)
    fid = file_type.id
    req = get_csrf_request_with_db()
    req.context = file_type
    view = FileTypeDeleteView(req)
    view()
    dbsession.flush()

    assert FileType.get(fid) is None
