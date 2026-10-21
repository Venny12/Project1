# Ingestion module - design notes (Week 2, Day 2)

Answer in your own words, 2-4 sentences each. Replace every line that starts with


## 1. Exceptions or assertions?
In `validate_record` I raise exceptions for a negative duration, but in
`IngestionReport.check_invariants` I use `assert`. Why is each the right tool there?

In validate_record I raisw exceptions because a negative duration is invalid input data, and the code should handle it without stopping or terminating.

In IngestionReport.check_invariants I use assert because it checks if the code is correct or not, such as the total number of valid and rejected records equals the rows_seen, it will help to identify if any code mistakes.

## 2. Stop or collect?
Why is a malformed JSON file a `SourceError` that stops loading, while a record with
a bad status is a `RecordValidationError` that is collected? Who benefits from this split?

A malformed JSON file raises a SourceError because the file can't be parsed properly.

A record with an bad status is a RecordValidationError because only that particular record is incorrect. This helps to identity errors without losing correct data.

## 3. What did the context managers buy you?
Name two things that `open_source` / `LoadSession` do for the caller that you would otherwise
have to remember to do at every call site.

The open_source context manager automatically closes the file after reading, so we don't have to close it everytime. Loadsession tracks the execution time and whether the loading operation completed or failed.

## 4. Your hardest bad-input case
Which sample file or record took you longest to handle, and what was the cause?

The folder being passed instead of a file was difficult for me to handle.