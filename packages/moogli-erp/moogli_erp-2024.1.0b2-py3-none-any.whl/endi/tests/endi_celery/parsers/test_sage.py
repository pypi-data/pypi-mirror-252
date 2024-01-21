import datetime
from endi_celery.parsers.sage import (
    CsvFileParser,
    SlkFileParser,
    OperationProducer,
)


def test_metadata(data_dir):
    parser = CsvFileParser(data_dir.joinpath("2017_09_grand_livre.csv"))
    metadata = parser.metadata()
    assert metadata.filename == "2017_09_grand_livre.csv"
    assert metadata.date == datetime.date(2017, 9, 1)
    assert metadata.filetype == "general_ledger"

    parser = CsvFileParser(data_dir.joinpath("general_ledger_2017_09_grand_livre.csv"))
    metadata = parser.metadata()
    assert metadata.filename == "general_ledger_2017_09_grand_livre.csv"
    assert metadata.date == datetime.date(2017, 9, 1)
    assert metadata.filetype == "general_ledger"


class TestCsvFileParser:
    def test_stream(self, data_dir):
        parser = CsvFileParser(data_dir.joinpath("2017_09_grand_livre.csv"))
        streamed = parser.stream()
        assert next(streamed) == [
            "01USER",
            "431000",
            "29/11/13",
            "SAL",
            "8819",
            "Libellé",
            "",
            "4.8",
            "",
            "4.8",
        ]


class TestSlkFileParser:
    def test_stream(self, data_dir):
        parser = SlkFileParser(data_dir.joinpath("2017_09_grand_livre.slk"))
        streamed = parser.stream()
        assert next(streamed) == [
            "01USER",
            "431000",
            "29/11/13",
            "SAL",
            "8819",
            "Libellé",
            " ",
            "4.8",
            " ",
            "4.8",
        ]


class TestOperationProducer:
    def test_get_label(self, data_dir):
        producer = OperationProducer(
            CsvFileParser(data_dir.joinpath("2017_09_grand_livre.csv"))
        )
        label = producer._get_label(
            [
                "",
                "",
                "",
                "",
                "",
                "Label With more than 80 characters are too long for the enDI database,"
                " we should truncate them beforecreating db objects",
            ]
        )
        assert len(label) == 80

    def test__stream_operation(self, data_dir):
        producer = OperationProducer(
            CsvFileParser(data_dir.joinpath("2017_09_grand_livre.csv"))
        )
        op = producer._stream_operation(
            [
                "01USER",
                "431000",
                "29/11/13",
                "SAL",
                "8819",
                "Libellé",
                " ",
                "4.8",
                " ",
                "4.8",
            ]
        )
        assert op.analytical_account == "01USER"
        assert op.general_account == "431000"
        assert op.date == datetime.date(2013, 11, 29)
        assert op.label == "Libellé"
        assert op.debit == 0
        assert op.credit == 4.8
