from endi.utils.ascii import force_filename


class TestPdfFromHtmlService:
    def _init_service(self, context, get_csrf_request_with_db, user, pdf_config):
        from endi.views.task.pdf_rendering_service import (
            TaskPdfFromHtmlService,
        )

        request = get_csrf_request_with_db(
            request_config=pdf_config, user=user, context=context
        )
        service = TaskPdfFromHtmlService(context, request)
        return service

    def test_render_returns_pdf(
        self,
        full_invoice,
        get_csrf_request_with_db,
        user,
        pdf_config,
        dbsession,
        mk_business_type,
    ):
        service = self._init_service(
            full_invoice, get_csrf_request_with_db, user, pdf_config
        )
        pdf = service.render()
        assert hasattr(pdf, "seek")

    def test_get_facturx_xml(
        self, full_invoice, get_csrf_request_with_db, user, pdf_config
    ):
        from facturx import check_facturx_xsd

        service = self._init_service(
            full_invoice, get_csrf_request_with_db, user, pdf_config
        )
        xml_string = service._get_facturx_xml()
        assert check_facturx_xsd(xml_string)

    def test_filename(
        self,
        full_invoice,
        full_estimation,
        get_csrf_request_with_db,
        user,
        pdf_config,
        mk_config,
    ):
        service = self._init_service(
            full_estimation, get_csrf_request_with_db, user, pdf_config
        )
        fname = service.filename()
        assert fname == "devis_brouillon_{}.pdf".format(full_estimation.id)

        full_estimation.status = "valid"
        fname = service.filename()
        assert fname == "devis_{}.pdf".format(
            force_filename((full_estimation.internal_number))
        )

        service = self._init_service(
            full_invoice, get_csrf_request_with_db, user, pdf_config
        )
        fname = service.filename()
        assert fname == "facture_brouillon_{}.pdf".format(full_invoice.id)

        full_invoice.status = "valid"
        full_invoice.official_number = "num 257"
        fname = service.filename()
        assert fname == "facture_num_257.pdf"

        mk_config("sale_pdf_filename_template", "{enseigne}_{numero}")
        service = self._init_service(
            full_invoice, get_csrf_request_with_db, user, pdf_config
        )
        fname = service.filename()
        assert fname == "company_num_257.pdf"
