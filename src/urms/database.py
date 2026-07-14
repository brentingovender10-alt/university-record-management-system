"""
Database access layer for the front end.

This is the single integration seam between the Streamlit interface and the
database.  Every screen and query in the app talks to the database through the
helpers here - no page runs raw SQL against a connection directly.

Connection strategy
--------------------
1. If ``database/university.db`` exists (the file produced from the frontend), the app connects to it read-only.
2. Otherwise it falls back to an in-memory demo database built from a demo database
   ``demo_db.py`` to allow a visualisation of the front end interface.

The active source is exposed via :func:`data_source_label` so the UI can show
which database it is using.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
try:
    import streamlit as st
except Exception:
    st = None

if st is not None and hasattr(st, "cache_resource"):
    _cache_resource = st.cache_resource
else:
    def _cache_resource(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

from . import demo_db

# database/university.db sits two levels up from this file: src/urms/ -> repo/database
_REAL_DB_PATH = Path(__file__).resolve().parents[2] / "database" / "university.db"


@_cache_resource(show_spinner=False)
def get_connection():
    """Return a cached SQLite connection (real DB if present, else demo DB)."""
    if _REAL_DB_PATH.exists():
        import sqlite3

        conn = sqlite3.connect(f"file:{_REAL_DB_PATH}?mode=ro", uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    return demo_db.build_in_memory()


def using_real_db() -> bool:
    return _REAL_DB_PATH.exists()


def data_source_label() -> str:
    if using_real_db():
        return f"Connected to database/university.db"
    return "Demo data (in-memory) - real database/university.db not found yet"


def run_query(sql: str, params: tuple | dict | None = None) -> pd.DataFrame:
    """Execute a parametrised SELECT and return the result as a DataFrame."""
    conn = get_connection()
    return pd.read_sql_query(sql, conn, params=params or ())


def scalar(sql: str, params: tuple | dict | None = None):
    """Execute a query expected to return a single value."""
    df = run_query(sql, params)
    if df.empty:
        return None
    return df.iloc[0, 0]
