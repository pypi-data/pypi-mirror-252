import datetime
import os
import csv

from endi.tests.conftest import TMPDIR
from endi_payment.archive import FileArchiveService
from endi_payment.models import EndiPaymentArchiveSeal


class TestFileArchiveService:
    def test_archive(self, mk_payment_history, get_csrf_request_with_db):
        h1 = mk_payment_history(amount=2025, created_at=datetime.date(2019, 1, 1))
        id_ = h1.id
        pyramid_request = get_csrf_request_with_db()
        service = FileArchiveService(None, pyramid_request)
        seal = service.archive(h1)

        with open(service.filepath, "r") as fbuf:
            reader = csv.reader(fbuf)
            row = None
            for row in reader:
                pass

        assert row[0] == str(h1.id)
        assert row[5] == "2025"

        assert seal.endi_payment_history_id == id_
        assert seal.remote_identification_key == service._get_id_key(
            open(service.filepath, "rb").read()
        )
