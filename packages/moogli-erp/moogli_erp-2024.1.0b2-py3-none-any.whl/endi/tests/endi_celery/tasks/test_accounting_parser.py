from endi_celery.tasks.accounting_parser import _get_file_path_from_pool
from endi_celery.parsers.sage import (
    OperationProducer,
    CsvFileParser,
    SlkFileParser,
)
from endi_celery.tasks.accounting_parser import (
    _get_operation_producer,
    _get_file_parser,
    AccountingDataHandler,
)

from endi.models.accounting.operations import AccountingOperationUpload


def test_get_file_path_from_pool(data_dir):
    result = _get_file_path_from_pool(data_dir)

    assert result.name.startswith("2017_09")
    result = _get_file_path_from_pool(data_dir.joinpath("unnexistingdir"))
    assert result is None


def test__get_file_parser(request_with_config, data_dir):
    parser = _get_file_parser(
        request_with_config, data_dir.joinpath("2022_01_fichier.csv")
    )
    assert isinstance(parser, CsvFileParser)
    parser = _get_file_parser(
        request_with_config, data_dir.joinpath("2022_01_fichier.slk")
    )
    assert isinstance(parser, SlkFileParser)


def test__get_operation_producer(request_with_config, data_dir):

    parser = CsvFileParser(data_dir.joinpath("2022_01_fichier.csv"))

    producer = _get_operation_producer(request_with_config, parser)
    assert isinstance(producer, OperationProducer)


class TestAccountingDataHandler:
    def test_run(self, get_csrf_request_with_db, data_dir):
        parser = CsvFileParser(data_dir.joinpath("2017_09_grand_livre.csv"))
        producer = OperationProducer(parser)
        handler = AccountingDataHandler(parser, producer)
        upload_id = handler.run()[0]
        upload = AccountingOperationUpload.get(upload_id)
        assert len(upload.operations) == 10
