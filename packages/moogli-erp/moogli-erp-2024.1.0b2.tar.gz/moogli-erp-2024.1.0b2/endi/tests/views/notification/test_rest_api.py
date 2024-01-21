import datetime
from endi.views.notification.rest_api import NotificationRestApiView


class TestNotificationRestApi:
    def test_postpone(self, mk_notification, get_csrf_request_with_db, user):
        notif = mk_notification(due_date=datetime.date(2022, 1, 1), user_id=user.id)
        request = get_csrf_request_with_db(context=notif, user=user)
        view = NotificationRestApiView(notif, request)
        view.postpone_endpoint()
        assert notif.due_date == datetime.date.today() + datetime.timedelta(days=7)

    def test_mark_read(self, mk_notification, get_csrf_request_with_db, user):
        notif = mk_notification(user_id=user.id)
        request = get_csrf_request_with_db(context=notif, user=user)
        view = NotificationRestApiView(notif, request)
        view.mark_read_endpoint()
        assert notif.read
        assert len(view.collection_get()) == 0
