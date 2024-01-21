import pytest
from unittest.mock import MagicMock
from endi.models.progress_invoicing.services.status import (
    ChapterStatusService,
    BaseProductStatusService,
    ProductStatusService,
    WorkStatusService,
    WorkItemStatusService,
)


@pytest.fixture
def task(dbsession, user, project, customer, company):
    from endi.models.task import Task

    task = Task(user=user, company=company, project=project, customer=customer)
    dbsession.add(task)
    dbsession.flush()
    return task


class TestChapterStatusService:
    @pytest.fixture
    def chapter_status(self, mk_progress_invoicing_chapter_status):
        pass

    def test_sync_with_plan(self):
        pass


class TestBaseProductStatusService:
    @pytest.fixture
    def product_status(self, mk_progress_invoicing_product_status):
        return mk_progress_invoicing_product_status(percent_to_invoice=50)


class TestProductStatusService:
    pass


class TestWorkStatusService:
    pass


class TestWorkItemStatusService:
    pass
