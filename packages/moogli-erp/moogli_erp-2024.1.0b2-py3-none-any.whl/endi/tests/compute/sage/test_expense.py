import pytest
import datetime
from endi.compute.sage.expense import (
    BaseSageExpenseContribution,
    SageExpenseMain,
)


@pytest.fixture
def expense(mk_expense_sheet, mk_company, mk_user):
    company = mk_company(
        code_compta="COMP_ANA",
        general_expense_account="CGNDF",
    )
    user = mk_user(
        firstname="firstname",
        lastname="lastname",
        compte_tiers="COMP_TIERS",
    )

    return mk_expense_sheet(
        company=company,
        user=user,
        month=5,
        year=2014,
    )


@pytest.fixture
def sage_expense(config_request, expense, contribution_module):
    factory = SageExpenseMain(None, config_request)
    factory.set_expense(expense)
    return factory


@pytest.fixture
def expense_sheet_tva_on_margin(
    expense_sheet,
    mk_expense_line,
    expense_type_tva_on_margin,
    contribution_module,
):
    lines = [
        # One tva-on-margin
        mk_expense_line(
            type_id=expense_type_tva_on_margin.id,
            ht=1000,
            tva=200,
        ),
        # One regular
        mk_expense_line(
            ht=10000,
            tva=2000,
        ),
    ]
    for line in lines:
        expense_sheet.lines.append(line)

    return expense_sheet


@pytest.fixture
def sage_expense_tva_on_margin(config_request, expense_sheet_tva_on_margin):
    factory = SageExpenseMain(None, config_request)
    factory.set_expense(expense_sheet_tva_on_margin)
    return factory


@pytest.mark.expense
class TestSageExpenseMain:
    """
    Main Expense export module testing
    """

    def test_get_contribution(self, sage_expense, expense):
        assert sage_expense.get_contribution() == 10
        expense.company.contribution = 5
        assert sage_expense.get_contribution() == 5

    def test__get_contribution_amount(self, sage_expense, expense):
        assert sage_expense._get_contribution_amount(100) == 10
        expense.company.contribution = 5
        assert sage_expense._get_contribution_amount(100) == 5

    def test_base_entry(self, sage_expense):
        assert sage_expense.libelle == "Firstname LASTNAME/frais 5 2014"
        assert sage_expense.num_feuille == "ndf52014"
        assert sage_expense.code_journal == "JOURNALNDF"

        base_entry = sage_expense.get_base_entry()
        for i in ("code_journal", "num_feuille", "type_"):
            assert i in base_entry

    def test_tva_on_margin(self, sage_expense_tva_on_margin):
        entries = list(sage_expense_tva_on_margin.yield_entries())
        assert len(entries) == 10

        def _find(filter_dict, dictlist):
            # dictlist structure :[({},{}), ({},{}),…]
            res = []
            for i in dictlist:
                match = True
                for k, v in filter_dict.items():
                    # check only analytical line
                    if i[0].get(k) != v:
                        match = False
                        break
                if match:
                    res.append(i)

            return res

        # One for TVA in account dedicated to tva on margin
        assert (
            len(
                _find(
                    {"credit": 200, "compte_cg": "CG_TVA_OM"},
                    entries,
                )
            )
            == 1
        )

        # One with TTC of tva_on_margin expense line
        assert (
            len(
                _find(
                    {"debit": 1200},
                    entries,
                )
            )
            == 1
        )

        # One with HT of regular expense line
        assert (
            len(
                _find(
                    {"debit": 10000},
                    entries,
                )
            )
            == 1
        )

        # credit and debit compensate
        sum([i[1].get("credit", -i[1].get("debit", 0)) for i in entries]) == 0

    def test_credit(self, sage_expense):
        general, analytic = sage_expense._credit(
            2500000,
            libelle="Firstname                LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )
        assert analytic["type_"] == "A"
        assert analytic["credit"] == 2500000
        assert analytic["compte_cg"] == "CGNDF"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["compte_tiers"] == "COMP_TIERS"

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_debit_ht(self, sage_expense, expense_type):
        general, analytic = sage_expense._debit_ht(
            expense_type,
            150000,
            libelle="Firstname LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "ETYPE1"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["code_tva"] == "CODETVA"
        assert analytic["debit"] == 150000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_debit_tva(self, sage_expense, expense_type):
        general, analytic = sage_expense._debit_tva(
            expense_type,
            120000,
            libelle="Firstname LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "COMPTETVA"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["code_tva"] == "CODETVA"
        assert analytic["debit"] == 120000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_credit_company(self, sage_expense):
        general, analytic = sage_expense._credit_company(
            120000,
            libelle="Firstname                LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "CG_CONTRIB_DEBIT"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["credit"] == 120000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_debit_company(self, sage_expense):
        general, analytic = sage_expense._debit_company(
            120000,
            libelle="Firstname                LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "BANK_CG"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["debit"] == 120000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_credit_cae(self, sage_expense):
        general, analytic = sage_expense._credit_cae(
            120000,
            libelle="Firstname                LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "BANK_CG"
        assert analytic["num_analytique"] == "NUM_ANA"
        assert analytic["credit"] == 120000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_debit_cae(self, sage_expense):
        general, analytic = sage_expense._debit_cae(
            120000,
            libelle="Firstname                LASTNAME/frais 5 2014",
            date=sage_expense.date,
        )

        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "CG_CONTRIB_CREDIT"
        assert analytic["num_analytique"] == "NUM_ANA"
        assert analytic["debit"] == 120000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_credit_tva_on_margin(self, sage_expense, expense_type_tva_on_margin):
        general, analytic = sage_expense._credit_tva_on_margin(
            expense_type_tva_on_margin,
            50000000,
            libelle=sage_expense.libelle,
            date=sage_expense.date,
        )
        assert analytic["type_"] == "A"
        assert analytic["compte_cg"] == "CG_TVA_OM"
        assert analytic["num_analytique"] == "COMP_ANA"
        assert analytic["credit"] == 50000000

        assert general["type_"] == "G"
        assert "num_analytique" not in list(general.keys())

    def test_export_by_category(
        self,
        sage_expense,
        mk_expense_line,
        mk_expense_type,
    ):
        # On désactive le module de contribution
        sage_expense.contribution_module = None
        mk_expense_line(ht=100000, tva=20000, category="2", sheet=sage_expense.expense)
        mk_expense_line(ht=100000, tva=20000, category="2", sheet=sage_expense.expense)

        result = sage_expense.yield_entries(category="1")
        assert list(result) == []

        result = sage_expense.yield_entries(category="2")
        # 3 : pairs de lignes générales et analytiques HT TVA TTC
        # pour le module général
        result = list(result)
        assert len(result) == 3
        assert result[0][0]["credit"] == 240000
        assert result[1][0]["debit"] == 200000
        assert result[2][0]["debit"] == 40000

    def test_export_ungrouped_entries(
        self,
        sage_expense,
        mk_expense_line,
        mk_expense_type,
    ):
        # On désactive le module de contribution
        sage_expense.contribution_module = None
        mk_expense_line(ht=100000, tva=20000, category="2", sheet=sage_expense.expense)
        mk_expense_line(ht=100000, tva=20000, category="2", sheet=sage_expense.expense)

        result = sage_expense._yield_detailed_expenses(category="1")
        assert list(result) == []

        result = sage_expense._yield_detailed_expenses(category="2")
        # 3 : pairs de lignes générales et analytiques HT TVA TTC
        # pour le module général
        result = list(result)
        assert len(result) == 6
        assert result[0][0]["credit"] == 120000
        assert result[1][0]["debit"] == 100000
        assert result[2][0]["debit"] == 20000
