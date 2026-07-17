"""Pytest configuration and fixtures for URMS tests."""

import pytest
import sqlite3
from unittest.mock import Mock, patch
from pathlib import Path

from src.urms import demo_db


@pytest.fixture
def demo_connection():
    """Create and return an in-memory demo database connection."""
    conn = demo_db.build_in_memory()
    yield conn
    conn.close()


@pytest.fixture
def demo_dataframe_result():
    """Example DataFrame result from a query."""
    import pandas as pd
    return pd.DataFrame({
        "Student ID": ["S001", "S002", "S003"],
        "Full Name": ["Alice Smith", "Bob Jones", "Carol White"],
        "Program": ["BSc Computer Science", "BSc Computer Science", "BSc Computer Science"],
        "Year": [2, 3, 1]
    })


@pytest.fixture
def mock_streamlit_cache():
    """Mock Streamlit's cache_resource decorator."""
    def decorator(func):
        return func
    
    with patch('streamlit.cache_resource', decorator):
        yield


@pytest.fixture
def mock_real_db_missing(tmp_path):
    """Mock scenario where real database does not exist."""
    with patch('src.urms.database._REAL_DB_PATH', tmp_path / "nonexistent.db"):
        yield


@pytest.fixture
def mock_real_db_exists(tmp_path):
    """Mock scenario where real database exists."""
    # Create a minimal valid SQLite database
    db_file = tmp_path / "university.db"
    conn = sqlite3.connect(str(db_file))
    conn.execute("CREATE TABLE STUDENT (StudentID TEXT PRIMARY KEY, FullName TEXT)")
    conn.execute("INSERT INTO STUDENT VALUES ('S001', 'Test Student')")
    conn.commit()
    conn.close()
    
    with patch('src.urms.database._REAL_DB_PATH', db_file):
        yield db_file


@pytest.fixture
def enrollment_data():
    """Sample enrollment data from demo database."""
    return [
        {"StudentID": "S001", "OfferingID": 1, "GradeLetter": "A", "FinalGradePercent": 85.0},
        {"StudentID": "S001", "OfferingID": 2, "GradeLetter": "B", "FinalGradePercent": 78.0},
        {"StudentID": "S002", "OfferingID": 2, "GradeLetter": "A", "FinalGradePercent": 90.0},
        {"StudentID": "S002", "OfferingID": 4, "GradeLetter": "B", "FinalGradePercent": 75.0},
        {"StudentID": "S004", "OfferingID": 3, "GradeLetter": "A", "FinalGradePercent": 88.0},
        {"StudentID": "S009", "OfferingID": 7, "GradeLetter": "A", "FinalGradePercent": 95.0},
    ]


@pytest.fixture
def student_data():
    """Sample student data from demo database."""
    return [
        {"StudentID": "S001", "FullName": "Alice Smith", "YearOfStudy": 2, "ProgramID": 1},
        {"StudentID": "S002", "FullName": "Bob Jones", "YearOfStudy": 3, "ProgramID": 1},
        {"StudentID": "S003", "FullName": "Carol White", "YearOfStudy": 1, "ProgramID": 1},
        {"StudentID": "S004", "FullName": "David Brown", "YearOfStudy": 1, "ProgramID": 2},
        {"StudentID": "S005", "FullName": "Eva Green", "YearOfStudy": 4, "ProgramID": 3},
    ]
