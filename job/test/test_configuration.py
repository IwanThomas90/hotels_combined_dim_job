import json
import os
import pytest

from configuration import Configuration


@pytest.fixture(scope="function")
def config():
    config_file_path = os.path.join(os.path.dirname(__file__), 'test_config/test_config.ini')
    configuration = Configuration([config_file_path])
    return configuration


def test_get_value(config):
    assert config.get('warehouse_host') == 'localhost'


def test_print_as_json_valid_json(config, capsys):
    config.print_as_json()
    actual_output, err = capsys.readouterr()
    parsed_output = json.loads(actual_output)
    assert parsed_output['warehouse_host'] == 'localhost'


def test_print_as_json_redaction(config, capsys):
    config.print_as_json()
    actual_output, err = capsys.readouterr()
    parsed_output = json.loads(actual_output)
    assert parsed_output['mart_db_password'] == '***********'
