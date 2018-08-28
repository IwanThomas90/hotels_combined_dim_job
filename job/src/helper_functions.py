import json
import os
import pkg_resources
import sys
import traceback
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from configuration import Configuration


def get_sql_from_package(filename: str, replacements: dict=None, package_name: str='sql'):
    """Reads a sql file from a given package. Also applies any replacements specified.
    """
    if replacements is None:
        replacements = {}

    templated_sql = pkg_resources.resource_string(package_name, filename).decode("utf-8")
    sql = templated_sql.format_map(replacements)
    return sql


def get_connection(port: int) -> Engine:
    conn_string = 'postgresql://postgres:docker@localhost:{warehouse_port}/docker'
    conn_string = conn_string.format_map({'warehouse_port': port})
    engine = create_engine(conn_string, isolation_level="AUTOCOMMIT")
    return engine


def get_mart_db_connection(config: Configuration) -> Engine:
    conn_string = 'postgresql://{mart_db_user}:{mart_db_password}@{warehouse_host}:{warehouse_port}/{mart_db_name}'
    conn_string = conn_string.format_map(config.as_dict())
    engine = create_engine(conn_string)
    return engine


def log_job_status(function_to_wrap):
    """A decorator that wraps the decorated function, catching any exceptions and printing the status afterwards
    """
    @wraps(function_to_wrap)
    def wrapper(*args, **kwargs):
        status_dict = {
            'errorMessage': None,
            'errorTrace': None,
            'success': True,
        }
        exit_code = 0
        try:
            function_to_wrap(*args, **kwargs)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback_list = [str(summary) for summary in traceback.extract_tb(exc_traceback)]
            status_dict['errorMessage'] = str(exc_value)
            status_dict['errorTrace'] = traceback_list
            status_dict['success'] = False
            exit_code = 1
        print(json.dumps(status_dict, sort_keys=True, indent=4))
        exit(exit_code)

    return wrapper


def print_version_from_file(file_name: str):
    """Prints the version of the app from the given file name. This should be in the same directory as this module
    If the file does not exist then the version will be shown to be 'UNDEFINED'
    """
    version = 'UNDEFINED'
    script_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(os.path.join(script_dir, file_name), 'r') as version_file:
            version = version_file.read()
    except FileNotFoundError:
        pass
    print('Job Version: {}'.format(version))
