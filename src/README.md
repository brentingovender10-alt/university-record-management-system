# Front end (Streamlit interface)

This folder contains the **front-end interface** for the University Record
Management System, built with [Streamlit](https://streamlit.io/).

## Run it

```bash
pip install -r src/requirements.txt
streamlit run src/Dashboard.py
```

The app opens in the browser. Use the sidebar to move between screens:
Dashboard, Students, Lecturers, Non-Academic Staff, Courses, Departments,
Programs, Research Projects, Query Builder and Reports.

## How it connects to the database

All data access goes through one module, **`urms/database.py`** - the single
integration point between the Streamlit front end and the database layer:

- If **`database/university.db`** exists (the file produced from the backend),
  the app uses it automatically, read-only.
- Otherwise it falls back to an **in-memory demo database** built from
  `urms/demo_db.py`, so the interface always runs and can be demonstrated on its
  own. The active source is shown at the bottom of the sidebar.

The front end was originally written against compact display names such as
`STUDENT`, `LECTURER`, `COURSE` and `PROGRAM`. The backend SQL schema in
`database/UniversityRecordManagementDatabase.sql` uses the final normalised
table names such as `students`, `lecturers`, `courses` and `programs`.
`urms/database.py` merges those layers by installing temporary compatibility
views when a real backend database is loaded. Those views map the backend
tables and columns into the shape expected by the Streamlit pages and Query
Builder.

This means the UI can keep its existing page/query code while still reading
from the backend schema. When the real `database/university.db` is added, the
interface picks it up automatically.

## Layout

```
src/
  Dashboard.py           Dashboard (entry point)
  pages/                 One file per sidebar screen (Streamlit multipage)
  urms/
    database.py          DB connection + backend compatibility views
    queries.py           The 10 Query Builder queries (parametrised SQL)
    demo_db.py           Illustrative schema + dummy data for standalone runs
    theme.py             Shared styling and table/card render helpers
  .streamlit/config.toml Theme
  requirements.txt
```

## Backend/front-end merge checks

The integration tests in `tests/test_database_integration.py` build an
in-memory database from `database/UniversityRecordManagementDatabase.sql`,
install the compatibility views, and verify that:

- the front-end relation names exist on the backend schema;
- all Query Builder queries execute against the backend schema;
- page-level SQL queries execute against the backend schema;
- the same compatibility views can be installed on a read-only
  `database/university.db` file.
