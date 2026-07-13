# Front end (Streamlit interface)

This folder contains the **front-end interface** for the University Record
Management System, built with [Streamlit](https://streamlit.io/).  .

## Run it

```bash
pip install -r src/requirements.txt
streamlit run src/Dashboard.py
```

The app opens in the browser. Use the sidebar to move between screens:
Dashboard, Students, Lecturers, Non-Academic Staff, Courses, Departments,
Programs, Research Projects, Query Builder and Reports.

## How it connects to the database

All data access goes through one module, **`urms/database.py`** — the single
integration seam with the database layer:

- If **`database/university.db`** exists (the file produced from the backend), 
the app uses it automatically, read-only.
- Otherwise it falls back to an **in-memory demo database** built from
  `urms/demo_db.py`, so the interface always runs and can be demonstrated on its
  own. The active source is shown at the bottom of the sidebar.

This keeps the front-end work independent of the backend: when the real
`university.db` is committed, the interface picks it up with no code changes.

## Layout

```
src/
  Dashboard.py           Dashboard (entry point)
  pages/                 One file per sidebar screen (Streamlit multipage)
  urms/
    database.py          DB connection + query helpers (integration seam)
    queries.py           The 10 Query Builder queries (parametrised SQL)
    demo_db.py           Illustrative schema + dummy data for standalone runs
    theme.py             Shared styling and table/card render helpers
  .streamlit/config.toml Theme
  requirements.txt
```

## Note on the schema / query contract

The table and column names used here follow the group-validated logical ERD. 
If the final database schema differs, only
`urms/demo_db.py` and `urms/queries.py` need to be reconciled with it — no page
code changes.
