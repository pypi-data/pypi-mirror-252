from endi.models.activity import (
    Event,
    Activity,
    Attendance,
)


def test_user_status():
    attendance = Attendance(account_id=1)
    attendance.status = "registered"
    a = Activity()
    a.attendances = [attendance]
    assert a.user_status(1) == "Attendu"
    assert a.user_status(2) == "Statut inconnu"

    assert a.is_participant(1)
    assert not a.is_participant(2)
