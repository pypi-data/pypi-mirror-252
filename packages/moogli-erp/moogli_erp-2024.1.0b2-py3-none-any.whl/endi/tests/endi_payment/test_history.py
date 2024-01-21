import datetime
import time
from endi.tests.tools import Dummy
from endi_payment.models import EndiPaymentHistory
from endi_payment.history import HistoryDBService


class TestHistoryDBService:
    def test_get_hash(
        self,
        mk_payment_history,
        get_csrf_request_with_db_and_user,
    ):

        h1 = mk_payment_history(amount=1, created_at=datetime.date(2019, 1, 1))
        h2 = mk_payment_history(amount=2, created_at=datetime.date(2019, 1, 2))
        h3 = mk_payment_history(amount=3, created_at=datetime.date(2019, 1, 3))

        pyramid_request = get_csrf_request_with_db_and_user()
        service = HistoryDBService(None, pyramid_request)
        assert service.get_previous_entry_hash() == h3.get_hash()
        assert service.get_previous_entry_hash() != h1.get_hash()

    def test_record(
        self,
        mk_payment_history,
        get_csrf_request_with_db_and_user,
        login,
        dbsession,
    ):
        h1 = mk_payment_history(amount=1, created_at=datetime.date(2019, 1, 1))
        h2 = mk_payment_history(amount=2, created_at=datetime.date(2019, 1, 2))
        h3 = mk_payment_history(amount=3, created_at=datetime.date(2019, 1, 3))

        pyramid_request = get_csrf_request_with_db_and_user()
        service = HistoryDBService(None, pyramid_request)

        payment = Dummy(
            id=2,
            mode="chèque",
            amount=4,
            bank_remittance_id=1,
            date=datetime.date.today(),
            bank=Dummy(compte_cg="cg"),
            tva=Dummy(value=2000),
        )
        invoice = Dummy(id=2, pdf_file_hash="hash")

        service.record("ADD", invoice, payment)
        result = dbsession.query(EndiPaymentHistory).all()[-1]
        assert dbsession.query(EndiPaymentHistory).count() == 4

        assert result.payment_id == 2
        assert result.previous_entry_hash == h3.get_hash()
