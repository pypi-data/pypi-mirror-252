class TestUserDatasFileGeneration:
    def _get_view(self, userdatas, get_csrf_request_with_db):
        from endi.views.userdatas.py3o import UserDatasFileGeneration

        req = get_csrf_request_with_db(
            current_route_path="/users",
        )
        req.context = userdatas
        view = UserDatasFileGeneration(req)
        return view

    def test_success(self, userdatas, get_csrf_request_with_db):
        view = self._get_view(
            userdatas,
            get_csrf_request_with_db,
        )
        res = view.__call__()
        assert res["current_userdatas"].coordonnees_lastname == "Userdatas"
        assert res["current_userdatas"].coordonnees_firstname == "userdatas"
        assert res["current_userdatas"].coordonnees_email1 == "userdatas@test.fr"
        assert (
            res["current_userdatas"].activity_companydatas[0].title == "test enseigne"
        )
        assert res["current_userdatas"].activity_companydatas[0].name == "test enseigne"
        assert (
            res["current_userdatas"].career_paths[0].hourly_rate_string
            == "Vingt quatre euros"
        )
        assert res["current_userdatas"].career_paths[0].num_hours == 151.00
        assert res["current_userdatas"].career_paths[0].taux_horaire == 24.00
        assert res["current_userdatas"].career_paths[0].parcours_salary == 3624.00
        assert res["templates"] == []
