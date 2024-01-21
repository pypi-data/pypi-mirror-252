import io
import hashlib


class TestPdfFileDepotStorageService:
    def _init_service(self, context, get_csrf_request_with_db, user):
        from endi.views.task.pdf_storage_service import (
            PdfFileDepotStorageService,
        )

        request = get_csrf_request_with_db(context=context, user=user)
        return PdfFileDepotStorageService(context, request)

    def test_store_pdf(self, full_invoice, get_csrf_request_with_db, user):
        service = self._init_service(full_invoice, get_csrf_request_with_db, user)
        pdf_buffer = io.BytesIO()
        pdf_buffer.write(b"PDF Datas")
        pdf_buffer.seek(0)

        full_invoice.status = "draft"
        service.store_pdf("Invoice number 1", pdf_buffer)
        assert full_invoice.pdf_file_id is None

        full_invoice.status = "valid"
        service.store_pdf("Invoice number 1", pdf_buffer)
        assert full_invoice.pdf_file_id is not None
        assert full_invoice.pdf_file_hash == hashlib.sha1(b"PDF Datas").hexdigest()

    def test_retrieve_pdf(self, full_invoice, get_csrf_request_with_db, user):
        service = self._init_service(full_invoice, get_csrf_request_with_db, user)

        assert service.retrieve_pdf() is None

        pdf_buffer = io.BytesIO()
        pdf_buffer.write(b"PDF Datas")
        pdf_buffer.seek(0)
        full_invoice.status = "valid"
        service.store_pdf("Invoice number 1", pdf_buffer)
        assert service.retrieve_pdf().read() == b"PDF Datas"
