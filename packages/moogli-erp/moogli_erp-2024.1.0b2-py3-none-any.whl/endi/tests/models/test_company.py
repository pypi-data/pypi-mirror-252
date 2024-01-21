def test_disable(company):
    company.disable()
    assert company.active == False


def test_enable(company):
    company.enable()
    assert company.active == True


def test_company_general_customer_account(company3):
    assert company3.general_customer_account == "00099988"


def test_company_third_party_customer_account(company3):
    assert company3.third_party_customer_account == "00055566"


def test_company_general_supplier_account(company3):
    assert company3.general_supplier_account == "0002332415"


def test_company_third_party_supplier_account(company3):
    assert company3.third_party_supplier_account == "000056565656"


def test_account_cascading(mk_company):
    from endi.models.config import Config

    for prefix in ("", "internal"):
        for key in (
            "third_party_customer_account",
            "general_customer_account",
            "third_party_supplier_account",
            "general_supplier_account",
        ):
            company = mk_company()
            cae_key = "%scae_%s" % (prefix, key)
            value = "CAE%s" % key
            Config.set(cae_key, value)

            method = getattr(company, "get_%s" % key)
            assert method(prefix) == "CAE%s" % key
            setattr(company, "%s%s" % (prefix, key), "COMP%s" % key)
            assert method(prefix) == "COMP%s" % key


def test_account_cascading_general_expense_account(company):
    from endi.models.config import Config

    Config.set("compte_cg_ndf", "CGNDF")
    assert company.get_general_expense_account() == "CGNDF"
    company.general_expense_account = "CGCOMPANY"
    assert company.get_general_expense_account() == "CGCOMPANY"
