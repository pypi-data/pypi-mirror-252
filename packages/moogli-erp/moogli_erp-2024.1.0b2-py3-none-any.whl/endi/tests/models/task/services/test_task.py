import pytest
import datetime
from endi.models.task.services import (
    TaskService,
)


from endi.models.task import Task


@pytest.fixture
def task_insurance_option(mk_task_insurance_option):
    return mk_task_insurance_option(rate=6)


@pytest.fixture
def task(
    dbsession,
    tva,
    product,
    customer,
    project,
    user,
    company,
    phase,
    mk_task_line,
    mk_business_type,
    mk_task_mention,
):
    result = Task(
        project=project,
        customer=customer,
        company=company,
        user=user,
        phase=phase,
        start_date=datetime.date(2021, 2, 1),
        first_visit=datetime.date(2021, 1, 20),
        end_date="Deux semaines après le début",
        business_type=mk_business_type(name="default"),
        mentions=[mk_task_mention(label="label1"), mk_task_mention(label="label2")],
    )
    result.line_groups[0].lines.append(mk_task_line(group=result.line_groups[0]))
    dbsession.add(result)
    dbsession.flush()
    return result


@pytest.fixture
def valid_status_log_entry(mk_status_log_entry, task, user):
    return mk_status_log_entry(
        node_id=task.id,
        status="valid",
        user_id=user.id,
        state_manager_key="status",
    )


@pytest.fixture
def draft_status_log_entry(mk_status_log_entry, task, user2):
    return mk_status_log_entry(
        node_id=task.id,
        status="draft",
        user_id=user2.id,
        state_manager_key="status",
    )


class TestTaskService:
    def test_duplicate(
        self,
        get_csrf_request_with_db,
        task,
        user,
        project,
        customer,
        phase,
        price_study,
        mk_price_study_product,
        mk_task_mention,
    ):
        mk_price_study_product(ht=100000)
        mk_price_study_product(ht=100000)
        mk_price_study_product(ht=100000)
        mk_price_study_product(ht=100000)
        price_study.sync_amounts(sync_down=True)
        disabled_mention = mk_task_mention(label="label3", active=False)
        task.mentions.append(disabled_mention)
        request = get_csrf_request_with_db()
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        for field in (
            "description",
            "mode",
            "display_units",
            "display_ttc",
            "expenses_ht",
            "workplace",
            "payment_conditions",
            "notes",
            "company",
            "customer",
            "project",
            "phase",
            "address",
            "insurance_id",
            "end_date",
        ):
            assert getattr(result, field) == getattr(task, field)
        assert result.status == "draft"
        assert result.owner == user
        assert result.status_user == user
        # Ref 3809
        for mention in task.mentions:
            if mention.active:
                assert mention in result.mentions
            else:
                assert mention not in result.mentions

        task.price_study = price_study
        project.project_type.include_price_study = False
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.price_study is None
        project.project_type.include_price_study = True
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.price_study is not None
        assert result.price_study != task.price_study
        # on a un chapter dans la price_study
        assert len(result.line_groups) == 1
        # On a 4 product
        assert len(result.line_groups[0].lines) == 4
        assert result.ht == 400000

    def test_duplicate_mode(
        self, get_csrf_request_with_db, task, user, project, customer, phase
    ):
        request = get_csrf_request_with_db()
        task.mode = "ttc"
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.mode == "ttc"
        task.mode = "ht"
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.mode == "ht"

    def test_duplicate_decimal_to_display(
        self,
        get_csrf_request_with_db,
        task,
        user,
        project,
        customer,
        phase,
        company,
    ):
        request = get_csrf_request_with_db()
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.decimal_to_display == 2
        company.decimal_to_display = 5
        result = TaskService.duplicate(
            request,
            task,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.decimal_to_display == 5

    def test_filter_by_validator_id_no_status(self, task, user, user2):
        assert TaskService.query_by_validator_id(Task, user2.id).count() == 0
        assert TaskService.query_by_validator_id(Task, user.id).count() == 0

    def test_filter_by_validator_id(
        self,
        task,
        draft_status_log_entry,
        valid_status_log_entry,
    ):
        validator_id = valid_status_log_entry.user_id
        draftor_id = draft_status_log_entry.user_id
        assert TaskService.query_by_validator_id(Task, draftor_id).count() == 0
        assert TaskService.query_by_validator_id(Task, validator_id).count() == 1
        assert TaskService.query_by_validator_id(Task, validator_id).first() == task

    def test_filter_by_validator_id_w_custom_query(
        self,
        task,
        valid_status_log_entry,
    ):
        validator_id = valid_status_log_entry.user_id
        query = Task.query().filter_by(official_number="DONOTEXIST")
        assert (
            TaskService.query_by_validator_id(Task, validator_id, query=query).count()
            == 0
        )

    def test_get_rate(
        self,
        dbsession,
        mk_custom_invoice_book_entry_module,
        task_insurance_option,
        task,
    ):
        mk_custom_invoice_book_entry_module(
            name="contribution", percentage=10, doctype="invoice"
        )
        mk_custom_invoice_book_entry_module(
            name="contribution", percentage=10, doctype="internalinvoice"
        )
        task.company.contribution = 5.25
        dbsession.merge(task.company)
        dbsession.flush()
        assert TaskService.get_rate(task, "contribution") == 5.25
        task.prefix = "internal"
        assert TaskService.get_rate(task, "contribution") == 10
        task.company.internalcontribution = 7.2
        dbsession.merge(task.company)
        dbsession.flush()
        assert TaskService.get_rate(task, "contribution") == 7.2
        task.prefix = ""
        assert TaskService.get_rate(task, "insurance") is None

        mk_custom_invoice_book_entry_module(
            name="insurance", percentage=10, doctype="invoice"
        )
        assert TaskService.get_rate(task, "insurance") == 10
        task.company.insurance = 8.1
        dbsession.merge(task.company)
        dbsession.flush()
        assert TaskService.get_rate(task, "insurance") == 8.1
        task.insurance = task_insurance_option
        dbsession.merge(task)
        dbsession.flush()
        assert TaskService.get_rate(task, "insurance") == 6

    def test_set_price_study(self, get_csrf_request_with_db, full_estimation):
        req = get_csrf_request_with_db()
        full_estimation.set_price_study(req)
        assert len(full_estimation.line_groups) == 1
        assert full_estimation.price_study is not None
        assert (
            full_estimation.price_study.chapters[0].task_line_group
            == full_estimation.line_groups[0]
        )

    def test__clean_task(
        self,
        get_csrf_request_with_db,
        full_estimation,
        mk_task_line_group,
        mk_task_line,
        mk_discount_line,
        tva,
    ):
        group1 = mk_task_line_group(task=full_estimation)
        mk_task_line(cost=100, tva=tva.value, group=group1)
        group2 = mk_task_line_group(task=full_estimation)
        mk_task_line(cost=100, tva=tva.value, group=group2)
        mk_discount_line(task=full_estimation)
        mk_discount_line(task=full_estimation)

        req = get_csrf_request_with_db()
        TaskService._clean_task(req, full_estimation)
        assert full_estimation.all_lines == []
        assert full_estimation.line_groups == []
        assert full_estimation.discounts == []
        assert full_estimation.total_ht() == 0
