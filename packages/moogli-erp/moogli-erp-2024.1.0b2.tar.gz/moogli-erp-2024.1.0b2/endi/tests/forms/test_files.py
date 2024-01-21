from endi.utils.image import ImageResizer
from endi.forms.files import SessionDBFileUploadTempStore


class TestSessionDBFileUploadTempStore:
    def test_filter_datas_issue_1148(self, get_csrf_request_with_db):
        # La validation du type de fichier est faite après le pré-filtrage
        # Si les fichiers déposés ne sont pas des images, ils ne sont pas
        # traités par les filtres et renvoyés tel quel
        request = get_csrf_request_with_db()
        filters = [ImageResizer(100, 100).complete]
        tmpstore = SessionDBFileUploadTempStore(request, filters)

        import io

        datas = io.BytesIO()
        datas.write(b"I'm not an image")
        datas.seek(0)
        result = tmpstore.filter_data(datas)
        assert result == datas
