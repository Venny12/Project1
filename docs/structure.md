qe-foundations/
|-- .gitignore
|-- README.md
|-- requirements.txt            <- runtime: requests
|-- requirements-dev.txt        <- "-r requirements.txt" + pytest
|-- smoke_utils.py              <- from starter_code (committed)
|-- check_exercise.py           <- from starter_code (committed)
|-- qe_foundations/
|   |-- __init__.py             <- __version__
|   `-- utils/
|       |-- __init__.py         <- re-exports the public API
|       |-- strings.py          <- normalize_whitespace, slugify, is_valid_email, mask_email (NEW)
|       |-- numbers.py          <- is_positive_int, clamp, percent
|       |-- dates.py            <- add_days, days_between (NEW), is_weekend, timestamp_for_filename
|       `-- data_gen.py         <- FIRST_NAMES, ROLES, make_users
|-- tests/.gitkeep              <- placeholder (Wed)
|-- data/.gitkeep               <- placeholder (Tue)
`-- docs/structure.md            