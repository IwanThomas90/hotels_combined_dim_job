import main
import os
import pytest
from unittest.mock import patch

from helper_functions import log_job_status, print_version_from_file

VERSION_FILE_NAME = 'TEST_VERSION'


@patch('builtins.exit')
def test_log_job_status_when_success(exit_mock, capsys):
    from helper_functions import log_job_status

    @log_job_status
    def wrapped_function(arg):
        print('running function with arg: {}'.format(arg))

    wrapped_function('test')

    actual_output, err = capsys.readouterr()
    expected_output = (
        "running function with arg: test\n"
        "{\n"
        "    \"errorMessage\": null,\n"
        "    \"errorTrace\": null,\n"
        "    \"success\": true\n"
        "}\n"
    )

    assert actual_output == expected_output
    exit_mock.assert_called_once_with(0)


@patch('traceback.extract_tb', return_value=['stack trace line 1', 'stack trace line 2'])
@patch('builtins.exit')
def test_log_job_status_when_fails(exit_mock, traceback_mock, capsys):

    @log_job_status
    def wrapped_function(arg):
        print('running function with arg: {}'.format(arg))
        raise InterruptedError('an error message')

    wrapped_function('test')

    actual_output, err = capsys.readouterr()
    expected_output = (
        "running function with arg: test\n"
        "{\n"
        "    \"errorMessage\": \"an error message\",\n"
        "    \"errorTrace\": [\n"
        "        \"stack trace line 1\",\n"
        "        \"stack trace line 2\"\n"
        "    ],\n"
        "    \"success\": false\n"
        "}\n"
    )

    assert actual_output == expected_output
    exit_mock.assert_called_once_with(1)


@pytest.fixture(scope="function")
def create_version_file(request):
    dir = os.path.dirname(main.__file__)
    file = open(os.path.join(dir, VERSION_FILE_NAME), 'w')
    file.write('1.0.99')
    file.close()

    def cleanup():
        os.remove(file.name)

    request.addfinalizer(cleanup)


@pytest.fixture(scope="function")
def delete_version_file():
    dir = os.path.dirname(main.__file__)
    file_path = os.path.join(dir, VERSION_FILE_NAME)
    if os.path.isfile(file_path):
        os.remove(file_path)


@pytest.mark.usefixtures("create_version_file")
def test_print_version_when_file_does_exist(capsys):
    print_version_from_file(VERSION_FILE_NAME)
    actual_output, err = capsys.readouterr()
    assert actual_output == 'Job Version: 1.0.99\n'


@pytest.mark.usefixtures("delete_version_file")
def test_print_version_when_file_does_not_exist(capsys):
    print_version_from_file(VERSION_FILE_NAME)
    actual_output, err = capsys.readouterr()
    assert actual_output == 'Job Version: UNDEFINED\n'
