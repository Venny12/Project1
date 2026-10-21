"""qe_foundations/ingestion/loader.py  -  TASK 6 (about 30 min)

Ties everything together:
    file -> reader (format) -> validate_record (rules) -> IngestionReport

Error POLICY (the heart of the milestone):
    SourceError            -> the whole file is unusable -> let it propagate (raise)
    RecordValidationError  -> one record is bad          -> COLLECT it and carry on

Already done for you: the IngestionReport and BatchResult classes' constructors
and the READERS lookup table. You write the TODOs.
"""

import csv
from pathlib import Path

from .contexts import LoadSession
from .exceptions import (
    DuplicateIdError,
    RecordValidationError,
    SourceError,
    SourceNotFoundError,
    UnsupportedFormatError,
)
from .readers import read_csv_records, read_json_records, read_xml_records
from .validation import validate_record

# Which reader handles which file extension (always compare lower-case suffixes).
READERS = {
    ".csv": read_csv_records,
    ".json": read_json_records,
    ".xml": read_xml_records,
}


class IngestionReport:
    """Result of loading ONE file: the valid records AND every rejected one."""

    def __init__(self, source, rows_seen=0):
        self.source = source
        self.rows_seen = rows_seen
        self.valid = []       # clean dicts returned by validate_record
        self.rejected = []    # RecordValidationError instances

    def summary(self):
        return( f"{Path(self.source).name}: {self.rows_seen} rows seen, "
            f"{len(self.valid)} valid, {len(self.rejected)} rejected")
        
        """TODO (6A): one line, EXACTLY this shape:

            test_cases_messy.csv: 10 rows seen, 3 valid, 7 rejected
        """
        #raise NotImplementedError("Task 6A: write IngestionReport.summary")

    def rejected_rows(self):
        return [
            {
                "source": Path(self.source).name,
                "row": error.row,
                "field": error.field,
                "reason": str(error),
            }
            for error in sorted(self.rejected, key=lambda e: e.row)
        ]
        """TODO (6A): the rejected records as plain dicts, ordered by row number.

        Each dict has exactly the keys: "source", "row", "field", "reason"
        ("reason" is the text of the exception, str(error)).
        """
        #raise NotImplementedError("Task 6A: write IngestionReport.rejected_rows")

    def check_invariants(self):
        assert len(self.valid) + len(self.rejected) == self.rows_seen, ("valid and rejected counts must equal rows_seen")

        ids = [record["id"] for record in self.valid]
        assert len(ids) == len(set(ids)), ("Valid records must not contain duplicate IDs")

        assert all(isinstance(error, RecordValidationError)
            for error in self.rejected
        ), ("Rejected entries must be RecordValidationError instances")

        """ (6B): use `assert` statements to check OUR OWN bookkeeping.

        Three invariants (README Task 6B). Each assert gets a helpful message.
        A failure here would be a BUG in this module, not bad input data.
        """
        #raise NotImplementedError("Task 6B: write IngestionReport.check_invariants")


class BatchResult:
    """Result of loading a whole folder."""

    def __init__(self):
        self.reports = []           # IngestionReport, one per file that could be read
        self.failed_sources = []    # SourceError instances, one per unusable file

    def totals(self):
        return {
            "files_ok": len(self.reports),
            "files_failed": len(self.failed_sources),
            "valid": sum(len(report.valid) for report in self.reports),
            "rejected": sum(len(report.rejected) for report in self.reports),
        }
        """TODO (6D): return a dict with exactly these keys:

            "files_ok", "files_failed", "valid", "rejected"
        """
        #raise NotImplementedError("Task 6D: write BatchResult.totals")


def load_test_cases(path):
        path = Path(path)
        
        with LoadSession(path):
            suffix = path.suffix.lower()
            if suffix not in READERS:
                raise UnsupportedFormatError(path, suffix)
            
            reader = READERS[suffix]
            raw_records = reader(path)
            
            report = IngestionReport(path.name, rows_seen=len(raw_records))
            seen_ids = set()

            for row, raw in enumerate(raw_records, start=1):
                try:
                    record = validate_record(row, raw)

                    if record["id"] in seen_ids:
                        raise DuplicateIdError(row, record["id"])

                except RecordValidationError as error:
                    report.rejected.append(error)

                else:
                    seen_ids.add(record["id"])
                    report.valid.append(record)

        report.check_invariants()
        return report
    
"""Load one CSV/JSON/XML file into an IngestionReport (6C).

    * Wrap the whole job in `with LoadSession(path):`
    * unknown extension -> raise UnsupportedFormatError
    * SourceError subclasses from the readers must propagate unchanged
    * rows are numbered from 1 (the header line of a CSV does not count)
    * bad records are COLLECTED in report.rejected, good ones go to report.valid
    * a repeated id -> DuplicateIdError for the LATER occurrence (the first one stays valid)
    * call report.check_invariants() before returning
    """
    #raise NotImplementedError("Task 6C: write load_test_cases")


def load_directory(folder):
    folder = Path(folder)

    if not folder.is_dir():
        raise SourceNotFoundError(folder)

    batch = BatchResult()

    for path in sorted(folder.iterdir(), key=lambda p: p.name):
        if not path.is_file():
            continue

        try:
            report = load_test_cases(path)

        except SourceError as error:
            batch.failed_sources.append(error)

        else:
            batch.reports.append(report)

    return batch
    """Load every file directly inside `folder` (TODO 6D).

    * sorted by file name; sub-folders are skipped
    * a bad FILE never stops the batch: collect its SourceError in failed_sources
    * a folder that does not exist (or is not a folder) -> raise SourceNotFoundError(folder)
    """
    #raise NotImplementedError("Task 6D: write load_directory")


def write_rejected_csv(report, out_path):
    out_path = Path(out_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["source", "row", "field", "reason"]
        )

        writer.writeheader()
        writer.writerows(report.rejected_rows())

    return out_path
    """Write report.rejected_rows() to a CSV file (TODO 6E) and return the Path.

    Header exactly: source,row,field,reason     (use csv.DictWriter)
    Create the parent folder if needed. Open the file with newline="".
    """
    #raise NotImplementedError("Task 6E: write write_rejected_csv")
