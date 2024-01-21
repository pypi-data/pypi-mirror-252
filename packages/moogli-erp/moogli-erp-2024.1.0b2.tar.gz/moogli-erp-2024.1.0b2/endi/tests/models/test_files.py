import io
from endi.models.files import File


def test_file_duplicate(dbsession):
    buf = io.BytesIO()
    data = b"Contenu de test"
    buf.write(data)
    f1 = File(name="test")
    f1.data = buf
    dbsession.add(f1)
    dbsession.flush()

    f2 = f1.duplicate()
    assert f2 != f1
    assert f2.data != f1.data
