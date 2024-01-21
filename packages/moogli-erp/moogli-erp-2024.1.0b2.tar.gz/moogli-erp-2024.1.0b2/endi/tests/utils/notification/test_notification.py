import pytest
import datetime
from pyramid_mailer import get_mailer
from endi.models.notification.notification import Notification
from endi.utils.notification.abstract import AbstractNotification
from endi.utils.notification.notification import (
    clean_notifications,
    notify,
    publish_event,
)
from endi.models.notification import NotificationEvent


@pytest.fixture
def mk_abstract():
    def _maker(**kw):
        default = {
            "key": "system:msg",
            "title": "Titre",
            "body": "Body",
        }
        default.update(kw)
        return AbstractNotification(**default)

    return _maker


def test_notify_due_datetime(get_csrf_request_with_db, mk_abstract, user):
    request = get_csrf_request_with_db()
    abstract = mk_abstract(
        due_datetime=datetime.datetime.now() + datetime.timedelta(days=50),
        context_tablename="career_stage",
        context_id=6,
    )
    notify(
        request,
        abstract,
        group_names=["manager"],
        user_ids=[1, 2, 3],
        follower_user_id=4,
        company_id=5,
    )
    event = NotificationEvent.query().filter_by(key="system:msg").first()
    assert event.title == "Titre"
    assert event.group_names == ["manager"]
    assert event.user_ids == [1, 2, 3]
    assert event.follower_user_id == 4
    assert event.company_id == 5
    assert event.context_tablename == "career_stage"
    assert event.context_id == 6

    abstract = mk_abstract(
        due_datetime=datetime.datetime.now(),
        context_tablename="career_stage",
        context_id=6,
    )
    notify(
        request,
        abstract,
        user_ids=[user.id],
    )
    assert not user.notifications
    event = NotificationEvent.query().filter_by(key="system:msg").all()[-1]
    publish_event(request, event)
    notif = user.notifications[0]
    assert notif.title == "Titre"
    assert notif.body == "Body"
    assert notif.due_date == datetime.date.today()
    assert notif.key == "system:msg"
    assert notif.status_type == "neutral"


def test_publish_event(
    get_csrf_request_with_db, mk_notification_event, user, mk_notification_event_type
):
    event = mk_notification_event(
        due_datetime=datetime.datetime.now(),
        user_ids=[user.id],
        title="test_publish_event",
    )
    request = get_csrf_request_with_db()
    publish_event(request, event)
    assert user.notifications[0].title == "test_publish_event"
    assert event.published

    # On définit le type avec un channel par défaut à 'mail'
    mk_notification_event_type(default_channel_name="email")
    event = mk_notification_event(
        due_datetime=datetime.datetime.now(),
        user_ids=[user.id],
        title="test_publish_event",
    )
    request = get_csrf_request_with_db()
    publish_event(request, event)
    mailer = get_mailer(request)
    assert len(mailer.outbox) == 1


def test_clean_read_notifications(
    get_csrf_request_with_db, mk_notification_event, mk_notification
):
    request = get_csrf_request_with_db()
    event = mk_notification_event(published=True)
    for i in range(5):
        notif = mk_notification(
            event=event, read=True, title="test_clean_read_notifications"
        )
        event.notifications.append(notif)
        request.dbsession.merge(event)
        request.dbsession.flush()

    clean_notifications(request)
    assert (
        Notification.query().filter_by(title="test_clean_read_notifications").count()
        == 0
    )


def test_clean_notvalid_notifications(
    get_csrf_request_with_db, mk_notification_event, mk_notification
):
    request = get_csrf_request_with_db()
    event = mk_notification_event(check_query="select 0;", published=True)
    for i in range(5):
        notif = mk_notification(
            event=event, read=False, title="test_clean_read_notifications"
        )
        event.notifications.append(notif)
        request.dbsession.merge(event)
        request.dbsession.flush()

    clean_notifications(request)
    assert (
        Notification.query().filter_by(title="test_clean_read_notifications").count()
        == 0
    )
