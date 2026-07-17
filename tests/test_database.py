"""Test cases for database.py module."""

import pytest
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock

from src.urms import database, demo_db


class TestGetConnection:
    """Tests for get_connection() function."""
    
    def test_get_connection_with_real_db(self, mock_real_db_exists):
        """TC-DB-001: get_connection() returns real DB connection when database exists."""
        # Clear the Streamlit cache to force re-initialization
        database.get_connection.clear()
        
        conn = database.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        # Verify row factory is set
        assert conn.row_factory is not None
    
    def test_get_connection_with_demo_db(self, mock_real_db_missing, mock_streamlit_cache):
        """TC-DB-002: get_connection() returns demo DB when real database missing."""
        database.get_connection.clear()
        
        conn = database.get_connection()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        
        # Verify demo tables exist
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='STUDENT'")
        assert cursor.fetchone() is not None
    
    def test_get_connection_caching(self, mock_real_db_missing, mock_streamlit_cache):
        """TC-DB-003: get_connection() returns cached connection on multiple calls."""
        database.get_connection.clear()
        
        conn1 = database.get_connection()
        conn2 = database.get_connection()
        
        # Same object reference due to caching
        assert conn1 is conn2


class TestUsingRealDb:
    """Tests for using_real_db() function."""
    
    def test_using_real_db_exists(self, mock_real_db_exists):
        """TC-DB-004: using_real_db() returns True when DB exists."""
        result = database.using_real_db()
        assert result is True
    
    def test_using_real_db_missing(self, mock_real_db_missing):
        """TC-DB-005: using_real_db() returns False when DB missing."""
        result = database.using_real_db()
        assert result is False


class TestDataSourceLabel:
    """Tests for data_source_label() function."""
    
    def test_data_source_label_real_db(self, mock_real_db_exists):
        """TC-DB-006: data_source_label() shows real DB connection message."""
        label = database.data_source_label()
        assert "database/university.db" in label
        assert "Connected" in label
    
    def test_data_source_label_demo_db(self, mock_real_db_missing):
        """TC-DB-007: data_source_label() shows demo DB message when real DB missing."""
        label = database.data_source_label()
        assert "Demo data" in label or "in-memory" in label


class TestRunQuery:
    """Tests for run_query() function."""
    
    def test_run_query_with_dict_params(self, demo_connection):
        """TC-DB-008: run_query() executes with dictionary parameters."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT StudentID, FullName FROM STUDENT WHERE StudentID = :sid",
                {"sid": "S001"}
            )
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert result.iloc[0]["FullName"] == "Alice Smith"
    
    def test_run_query_with_tuple_params(self, demo_connection):
        """TC-DB-010: run_query() executes with tuple parameters."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT StudentID, FullName FROM STUDENT WHERE StudentID = ?",
                ("S002",)
            )
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 1
            assert result.iloc[0]["FullName"] == "Bob Jones"
    
    def test_run_query_with_no_params(self, demo_connection):
        """TC-DB-012: run_query() executes without parameters."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT COUNT(*) as count FROM STUDENT"
            )
            assert isinstance(result, pd.DataFrame)
            assert result.iloc[0]["count"] == 12
    
    def test_run_query_empty_result(self, demo_connection):
        """TC-DB-009: run_query() returns empty DataFrame when no rows match."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT * FROM STUDENT WHERE StudentID = ?",
                ("INVALID_ID",)
            )
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 0
    
    def test_run_query_with_null_params(self, demo_connection):
        """TC-DB-011: run_query() executes with None parameters (no params passed)."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT COUNT(*) as total FROM DEPARTMENT"
            )
            assert isinstance(result, pd.DataFrame)
            assert result.iloc[0]["total"] == 4
    
    def test_run_query_returns_dataframe(self, demo_connection):
        """run_query() always returns a pandas DataFrame."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query("SELECT * FROM STUDENT LIMIT 1")
            assert isinstance(result, pd.DataFrame)
    
    def test_run_query_preserves_column_names(self, demo_connection):
        """run_query() preserves SQL column aliases in DataFrame."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT StudentID AS 'ID', FullName AS 'Name' FROM STUDENT LIMIT 1"
            )
            assert "ID" in result.columns
            assert "Name" in result.columns


class TestScalar:
    """Tests for scalar() function."""
    
    def test_scalar_single_value(self, demo_connection):
        """TC-DB-013: scalar() returns a single value from query result."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.scalar(
                "SELECT COUNT(*) FROM STUDENT"
            )
            assert result == 12
    
    def test_scalar_returns_none_for_empty_result(self, demo_connection):
        """TC-DB-014: scalar() returns None when query has no results."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.scalar(
                "SELECT StudentID FROM STUDENT WHERE StudentID = ?",
                ("NONEXISTENT",)
            )
            assert result is None
    
    def test_scalar_with_parameters(self, demo_connection):
        """TC-DB-015: scalar() executes with parameters correctly."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.scalar(
                "SELECT FullName FROM STUDENT WHERE StudentID = ?",
                ("S001",)
            )
            assert result == "Alice Smith"
    
    def test_scalar_returns_first_column(self, demo_connection):
        """scalar() returns value from first column only."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.scalar(
                "SELECT CourseCode, CourseName FROM COURSE LIMIT 1"
            )
            # Should return first column value
            assert isinstance(result, str)
            assert result in ["CS101", "CS201", "CS501", "CS301", "EE101", "BM101", "MA101"]


class TestIntegration:
    """Integration tests for database functions."""
    
    def test_run_query_and_scalar_consistency(self, demo_connection):
        """run_query() and scalar() return consistent data."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            # Get count via scalar
            count_scalar = database.scalar("SELECT COUNT(*) FROM STUDENT")
            
            # Get count via run_query
            df = database.run_query("SELECT COUNT(*) as cnt FROM STUDENT")
            count_df = df.iloc[0]["cnt"]
            
            assert count_scalar == count_df == 12
    
    def test_query_with_join(self, demo_connection):
        """run_query() handles JOIN queries correctly."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query("""
                SELECT s.StudentID, s.FullName, p.ProgramName
                FROM STUDENT s
                LEFT JOIN PROGRAM p ON s.ProgramID = p.ProgramID
                LIMIT 5
            """)
            assert isinstance(result, pd.DataFrame)
            assert len(result) > 0
            assert "ProgramName" in result.columns
    
    def test_query_with_where_clause(self, demo_connection):
        """run_query() filters results with WHERE clause."""
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(
                "SELECT * FROM STUDENT WHERE YearOfStudy = ?",
                (3,)
            )
            assert len(result) > 0
            assert all(result["YearOfStudy"] == 3)
