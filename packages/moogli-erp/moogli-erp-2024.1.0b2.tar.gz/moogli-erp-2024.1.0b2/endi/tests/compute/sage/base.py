import datetime


class BaseBookEntryTest:
    factory = None
    code_journal = "CODE_JOURNAL"

    def build_factory(self, config_request):
        return self.factory(None, config_request)

    def _test_product_book_entry(
        self,
        config_request,
        wrapped_invoice,
        method,
        exp_analytic_line,
        prod_cg="P0001",
        tva_cg="TVA0001",
        key=None,
    ):
        """
        test a book_entry output (one of a product)
        """
        wrapped_invoice.populate()
        book_entry_factory = self.build_factory(config_request)
        book_entry_factory.set_invoice(wrapped_invoice)
        if key is None:
            key = (prod_cg, tva_cg)
        product = wrapped_invoice.products[key]

        general_line, analytic_line = getattr(book_entry_factory, method)(product)

        exp_analytic_line["date"] = datetime.date(2013, 2, 2)
        exp_analytic_line["num_endi"] = wrapped_invoice.invoice.official_number
        exp_analytic_line["code_journal"] = self.code_journal
        exp_general_line = exp_analytic_line.copy()
        exp_analytic_line["type_"] = "A"
        exp_general_line["type_"] = "G"
        exp_general_line.pop("num_analytique", "")

        for key, value in general_line.items():
            if (
                not key.startswith("_") and key in exp_general_line
            ):  # ignore hidden entries
                print("Key : {}".format(key))
                print(value)
                print(exp_general_line[key])
                assert value == exp_general_line[key]
        for key, value in analytic_line.items():
            if (
                not key.startswith("_") and key in exp_analytic_line
            ):  # ignore hidden entries
                print(value)
                print(exp_analytic_line[key])
                assert value == exp_analytic_line[key]

    def _test_invoice_book_entry(
        self, config_request, wrapped_invoice, method, exp_analytic_line
    ):
        """
        test a book_entry output (one of a product)
        """
        wrapped_invoice.populate()
        book_entry_factory = self.build_factory(config_request)
        book_entry_factory.set_invoice(wrapped_invoice)
        general_line, analytic_line = getattr(book_entry_factory, method)()

        exp_analytic_line["date"] = datetime.date(2013, 2, 2)
        exp_analytic_line["num_endi"] = wrapped_invoice.invoice.official_number
        exp_analytic_line["code_journal"] = getattr(
            self, "code_journal", "CODE_JOURNAL"
        )
        exp_general_line = exp_analytic_line.copy()
        exp_analytic_line["type_"] = "A"
        exp_general_line["type_"] = "G"
        exp_general_line["_analytic_counterpart"] = analytic_line
        exp_analytic_line["_general_counterpart"] = general_line
        exp_general_line.pop("num_analytique", "")

        for key, value in general_line.items():
            if key not in exp_general_line:
                continue
            print("Key : {}".format(key))
            print(value)
            print(exp_general_line[key])
            assert value == exp_general_line[key]
        for key, value in analytic_line.items():
            if key not in exp_analytic_line:
                continue
            print(value)
            print(exp_analytic_line[key])
            assert value == exp_analytic_line[key]
