import pytest


@pytest.fixture
def company2(dbsession):
    from endi.models.company import Company

    comp = Company(name="New company", email="mail@company.fr")
    dbsession.add(comp)
    dbsession.flush()
    return comp


class TestCompanyAssociationView:
    def test_association(
        self, user, company, company2, get_csrf_request_with_db, config
    ):
        config.add_route("/users/{id}/companies", "/users/{id}/companies")
        from endi.views.user.company import CompanyAssociationView

        req = get_csrf_request_with_db(
            post={
                "submit": "submit",
                "formid": "deform",
                "companies": [company.name, company2.name],
            }
        )
        req.context = user
        view = CompanyAssociationView(req)
        result = view.__call__()
        assert result.code == 302
        assert result.location == "/users/{id}/companies".format(id=user.id)

        assert user.companies == [company, company2]
