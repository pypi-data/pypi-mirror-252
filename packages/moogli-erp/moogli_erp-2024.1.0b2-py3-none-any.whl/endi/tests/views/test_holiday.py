from endi.views.holiday import RestHoliday, get_holidays


def test_holiday(user, get_csrf_request_with_db):
    # Add
    request = get_csrf_request_with_db()
    request.context = user
    appstruct = {"start_date": "2013-04-15", "end_date": "2013-04-28"}
    request.json_body = appstruct
    view = RestHoliday(request)
    view.post()
    holidays = get_holidays(user_id=user.id).all()
    assert len(holidays) == 1

    # Add second one
    appstruct = {"start_date": "2013-04-01", "end_date": "2013-04-05"}
    request.json_body = appstruct
    view = RestHoliday(request)
    view.post()
    holidays = get_holidays(user_id=user.id).all()
    assert len(holidays) == 2

    # Delete
    request.matchdict["lid"] = holidays[1].id
    view = RestHoliday(request)
    view.delete()
    assert len(get_holidays(user_id=user.id).all()) == 1

    # edition + delete
    appstruct = {"start_date": "2013-04-13", "end_date": "2013-04-27"}
    request.json_body = appstruct
    request.matchdict["lid"] = holidays[0].id
    view = RestHoliday(request)
    view.put()

    holiday = get_holidays(user_id=user.id).all()[0]
    assert holiday.start_date.day == 13
