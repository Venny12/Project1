"""qe_foundations/ingestion/readers.py  -  TASK 4 (about 35 min)

One reader per format. Each returns a LIST OF RAW RECORDS and only deals with
FORMAT problems (is this valid CSV / JSON / XML? are the columns there?).
Business rules (is the status allowed? is the duration negative?) belong to
validation.py, NOT here.

Always open files through open_source() from contexts.py.
See README Task 4 for the exact contract of each reader.
"""

import csv
import json
import xml.etree.ElementTree as ET

from .contexts import open_source
from .exceptions import MalformedSourceError, MissingColumnsError
from .validation import REQUIRED_FIELDS


def read_csv_records(path):
    
    """CSV -> list of raw dicts, one per data row (use csv.DictReader)."""
    with open_source(path) as handle:
        reader = csv.DictReader(handle)
        headers = reader.fieldnames or []
        missing = [
            field for field in REQUIRED_FIELDS if field not in headers
        ]
        if missing:
            raise MissingColumnsError(path, missing)
        try:
            return list(reader)
        except csv.Error as error:
            raise MalformedSourceError(path, str(error)) from error


def read_json_records(path):
    """JSON -> list of raw records. Expected shape: {"suite": ..., "tests": [...]}."""
    with open_source(path) as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as error:
            raise MalformedSourceError(path, str(error)) from error
        
        if not isinstance(data, dict):
            raise MalformedSourceError(path, "JSON root must be an object")
        
        if "tests" not in data or not isinstance(data["tests"], list):
            raise MalformedSourceError(path, "JSON must contain a tests list")
        return data["tests"]

def read_xml_records(path):
    """XML -> list of raw dicts, one per <testcase> element at ANY depth."""
    
    with open_source(path) as handle:
        try:
            tree = ET.parse(handle)
        except ET.ParseError as error:
            raise MalformedSourceError(path, str(error)) from error
        root = tree.getroot()
        records = []
        for element in root.iter("testcase"):
            record = dict(element.attrib)

            for child in element:
                record[child.tag] = child.text.strip() if child.text is not None else None

            for field in REQUIRED_FIELDS:
                record.setdefault(field, None)

            records.append(record)

        return records

