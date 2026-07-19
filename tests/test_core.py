import sys
import sqlite3

sys.path.insert(0, 'src')

from urms import demo_db, database, queries
import pandas as pd


def test_demo_db_creation():
    conn = demo_db.build_in_memory()
    assert isinstance(conn, sqlite3.Connection)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STUDENT'")
    assert cur.fetchone() is not None


def test_database_run_query_and_scalar():
    # database.get_connection should return demo DB when real DB absent
    conn = database.get_connection()
    # run_query should return a DataFrame
    df = database.run_query('SELECT COUNT(*) AS cnt FROM STUDENT')
    assert isinstance(df, pd.DataFrame)
    assert 'cnt' in df.columns
    assert int(df['cnt'].iloc[0]) >= 1

    # scalar should return a single value
    val = database.scalar('SELECT ProgramName FROM PROGRAM WHERE ProgramID = ?', (1,))
    assert isinstance(val, str) and len(val) > 0


def test_query_no_params():
    # Query id 8 (Course enrolment counts) has no params
    spec = next(q for q in queries.QUERIES if q['id'] == 8)
    df = database.run_query(spec['sql'])
    assert isinstance(df, pd.DataFrame)
    assert 'Course Code' in df.columns or 'CourseCode' in df.columns


def test_query_named_param():
    # Query id 1 uses a named parameter :dept and bind returns a dict
    spec = next(q for q in queries.QUERIES if q['id'] == 1)
    params = spec['bind']({'dept': None})
    assert isinstance(params, dict)
    df = database.run_query(spec['sql'], params=params)
    assert isinstance(df, pd.DataFrame)
    # Should have student columns
    assert any(c.lower().startswith('student') for c in df.columns)


def test_query_positional_param_course():
    # Query id 2 uses a positional ? placeholder
    spec = next(q for q in queries.QUERIES if q['id'] == 2)
    # get a real course code from the demo DB
    code_df = database.run_query('SELECT CourseCode FROM COURSE LIMIT 1')
    course_code = code_df['CourseCode'].iloc[0]
    params = spec['bind']({'course': course_code})
    assert isinstance(params, tuple)
    df = database.run_query(spec['sql'], params=params)
    assert isinstance(df, pd.DataFrame)

