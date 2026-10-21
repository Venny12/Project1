"""qe_foundations/ingestion/validation.py  -  TASK 5 (about 25 min)

validate_record() decides whether ONE raw record is acceptable.

IMPORTANT: this is VALIDATION OF EXTERNAL DATA. Raise exceptions here.
Do NOT use `assert` in this file (assertions can be switched off with `python -O`).
See README Task 5 for the exact rules.
"""

from .exceptions import InvalidValueError, MissingFieldError

import math

REQUIRED_FIELDS = ("id", "title", "status", "duration")
VALID_STATUSES = ("pass", "fail", "blocked")


def validate_record(row, raw):
    """Turn one raw record into a clean dict, or raise a RecordValidationError.

    row : 1-based record number in the file (used in error messages)
    raw : whatever the reader produced for that record (usually a dict)

    Returns {"id": str, "title": str, "status": str, "duration": float}.
    """
    if not isinstance(raw, dict):
        raise InvalidValueError(row, "record", raw, "an object with the test fields")
    
    for name in REQUIRED_FIELDS:
        value = raw.get(name)
        if value is None or str(value).strip() == "":
            raise MissingFieldError(row, name)
    
    status = str(raw["status"]).strip().lower()
    
    if status not in VALID_STATUSES:
        raise InvalidValueError(row, "status", raw["status"], f"one of {VALID_STATUSES}")
    
    value = raw["duration"]
    if isinstance(value, bool):
        raise InvalidValueError(row, "duration", value, "a finite, non-negative number")
    
    try:
        duration = float(value)
    except (ValueError, TypeError):
        raise InvalidValueError(row, "duration", value, "a valid number") from None
    
    if not math.isfinite(duration) or duration < 0:
        raise InvalidValueError(
            row, "duration", value,
            "a finite, non-negative number"
        )

    return {
        "id": str(raw["id"]).strip(),
        "title": str(raw["title"]).strip(),
        "status": status,
        "duration": duration
    }