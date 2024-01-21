from endi.models.third_party.customer import Customer


def test_check_project_id(customer, project):
    assert Customer.check_project_id(customer.id, project.id)
    assert not Customer.check_project_id(customer.id, project.id + 1)


def test_get_general_account(customer, mk_company):
    customer.compte_cg = "TEST"
    assert customer.get_general_account() == "TEST"
    customer.compte_cg = None
    company = mk_company(
        general_customer_account="TEST2",
        internalgeneral_customer_account="TEST3",
    )
    customer.company = company
    assert customer.get_general_account() == "TEST2"
    assert customer.get_general_account(prefix="internal") == "TEST3"


def test_get_third_party_account(customer, mk_company):
    customer.compte_tiers = "TEST"
    assert customer.get_third_party_account() == "TEST"
    customer.compte_tiers = None
    company = mk_company(
        third_party_customer_account="TEST2",
        internalthird_party_customer_account="TEST3",
    )
    customer.company = company
    assert customer.get_third_party_account() == "TEST2"
    assert customer.get_third_party_account(prefix="internal") == "TEST3"
