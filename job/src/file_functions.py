import csv
import os
import re
import shutil
from collections import defaultdict
from typing import Dict

from exceptions import InvalidSchemaError, InvalidContentError


def validate_schema(header_row: list, type: str) -> None:
    hotel_headers = [
        'visitid', 'visitorid', 'createdon', 'brandid', 'label',
        'devicename', 'languagecode', 'clientplacename', 'clientcountrycode'
    ]

    # try:
    #     if type == 'visit':
    #         assert header_row == visit_headers
    #     if type == 'lead':
    #         assert header_row == lead_headers
    #     if type == 'booking':
    #         assert header_row == booking_headers
    # except AssertionError:
    #     raise InvalidSchemaError('Unexpected column headers in file')

    try:
        assert header_row == hotel_headers
    except AssertionError:
        raise InvalidSchemaError('Unexpected column headers in file')

def validate_content(content_dict: dict) -> None:
    """Checks whether file is empty

    Args:
        # to be updated
    """
    tmp = 1  # the header row
    pass

    # change the below
    # for file_type in ['booking', 'lead', 'visit']:
    #     length = len(content_dict[file_type])
    #     if length <= tmp:
    #         raise InvalidContentError('Empty or incorrect content for {} data.'.format(file_type))
    #     tmp = length
