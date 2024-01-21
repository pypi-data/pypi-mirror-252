"""
    Tests
"""
import os

from endi.tests.conftest import TMPDIR, DATASDIR
from endi.utils import fileupload


FAKEURL = "/assets/company/stuff"


def test_setitem(get_csrf_request):
    request = get_csrf_request()
    session = request.session
    tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL)
    assert tempstore.preview_url("dummy") is None
    # coming from database
    cstruct1 = {"uid": "test", "filename": "testfile1.jpg"}
    tempstore[cstruct1["uid"]] = cstruct1
    cstruct1["mimetype"] = None
    cstruct1["size"] = None
    assert tempstore.get(cstruct1["uid"]) == cstruct1
    assert tempstore.get(cstruct1["uid"])["preview_url"] == os.path.join(
        FAKEURL, cstruct1["filename"]
    )

    # just submitted
    cstruct2 = {
        "uid": "test",
        "filename": "testfile2.jpg",
        "fp": open(os.path.join(DATASDIR, "image.jpg"), "rb"),
        "mimetype": "image/jpeg",
        "size": 15,
    }
    tempstore[cstruct2["uid"]] = cstruct2
    assert tempstore.get(cstruct2["uid"])["mimetype"] == cstruct2["mimetype"]
    assert "fp" not in list(tempstore.get(cstruct2["uid"]).keys())
    assert os.path.isfile(os.path.join(TMPDIR, "testfile2.jpg")) is True
    assert tempstore.get(cstruct2["uid"])["preview_url"]
    assert os.path.join(FAKEURL, cstruct2["filename"])


def test_get_filepath(get_csrf_request):
    request = get_csrf_request()
    session = request.session
    tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL)
    assert tempstore.get_filepath("test") == os.path.join(TMPDIR, "test")


def test_filter(get_csrf_request):
    request = get_csrf_request()
    session = request.session

    def void(file_obj):
        file_obj.write(b"Nope")
        return file_obj

    filters = [void]

    tempstore = fileupload.FileTempStore(session, TMPDIR, FAKEURL, filters=filters)
    testfile = os.path.join(TMPDIR, "testfile")
    with open(testfile, "w+b") as f_obj:
        f_obj.write(b"There are some datas")

    cstruct2 = {
        "uid": "test",
        "filename": "testfile3.jpg",
        "fp": open(testfile, "w+b"),
        "mimetype": "image/jpeg",
        "size": 15,
    }
    tempstore[cstruct2["uid"]] = cstruct2
    # We verify the content has been passed through our filter before being
    # passed to the destination file
    content = open(os.path.join(TMPDIR, "testfile3.jpg"), "rb")
    assert content.read() == b"Nope"
