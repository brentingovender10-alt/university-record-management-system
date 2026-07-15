"""Test cases for queries.py module."""

import pytest
import pandas as pd
from unittest.mock import patch

from src.urms import queries, database


class TestQueryStructure:
    """Tests for QUERIES list structure."""
    
    def test_queries_list_exists(self):
        """TC-Q-001: QUERIES list is properly defined."""
        assert hasattr(queries, 'QUERIES')
        assert isinstance(queries.QUERIES, list)
        assert len(queries.QUERIES) == 10
    
    def test_query_has_required_fields(self):
        """Query entries have all required fields."""
        required_fields = ["id", "name", "description", "params", "sql", "bind"]
        for query in queries.QUERIES:
            for field in required_fields:
                assert field in query, f"Query missing field: {field}"
    
    def test_query_ids_unique(self):
        """All query IDs are unique."""
        ids = [q["id"] for q in queries.QUERIES]
        assert len(ids) == len(set(ids))
    
    def test_query_bind_is_callable(self):
        """Each query has a callable bind() function."""
        for query in queries.QUERIES:
            assert callable(query["bind"])


class TestQuery1StudentsByDepartment:
    """Tests for Query 1: Students by Department."""
    
    def test_query_1_with_department_filter(self, demo_connection):
        """TC-Q-002: Query 1 returns students filtered by department."""
        query = queries.QUERIES[0]
        assert query["id"] == 1
        assert query["name"] == "Students by Department"
        
        params = query["bind"]({"dept": 1})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Student ID" in result.columns
    
    def test_query_1_with_null_department(self, demo_connection):
        """TC-Q-003: Query 1 with None dept returns all students."""
        query = queries.QUERIES[0]
        params = query["bind"]({"dept": None})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 12  # All students in demo DB
    
    def test_query_1_columns(self, demo_connection):
        """Query 1 returns expected columns."""
        query = queries.QUERIES[0]
        params = query["bind"]({"dept": 1})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        expected_cols = ["Student ID", "Full Name", "Program", "Year"]
        assert list(result.columns) == expected_cols


class TestQuery2StudentEnrollment:
    """Tests for Query 2: Students Enrolled in a Course."""
    
    def test_query_2_valid_course(self, demo_connection):
        """TC-Q-004: Query 2 returns students enrolled in a course."""
        query = queries.QUERIES[1]
        assert query["id"] == 2
        
        params = query["bind"]({"course": "CS101"})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0
        assert "Student ID" in result.columns
        assert "Grade" in result.columns
    
    def test_query_2_invalid_course(self, demo_connection):
        """TC-Q-005: Query 2 with invalid course returns empty result."""
        query = queries.QUERIES[1]
        params = query["bind"]({"course": "INVALID999"})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) == 0


class TestQuery3LecturerCourses:
    """Tests for Query 3: Courses Taught by a Lecturer."""
    
    def test_query_3_valid_lecturer(self, demo_connection):
        """TC-Q-006: Query 3 returns courses taught by lecturer."""
        query = queries.QUERIES[2]
        assert query["id"] == 3
        
        params = query["bind"]({"lecturer": "L001"})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0


class TestQuery4ResearchExperts:
    """Tests for Query 4: Lecturers in a Research Area."""
    
    def test_query_4_valid_area(self, demo_connection):
        """TC-Q-007: Query 4 returns lecturers with research expertise."""
        query = queries.QUERIES[3]
        assert query["id"] == 4
        
        params = query["bind"]({"area": 1})  # Artificial Intelligence
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
        assert "Lecturer ID" in result.columns


class TestQuery5StudentsByYear:
    """Tests for Query 5: Students by Year of Study."""
    
    def test_query_5_year_1(self, demo_connection):
        """TC-Q-008: Query 5 returns year 1 students."""
        query = queries.QUERIES[4]
        assert query["id"] == 5
        
        params = query["bind"]({"year": 1})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
    
    def test_query_5_year_4(self, demo_connection):
        """TC-Q-009: Query 5 returns year 4 students."""
        query = queries.QUERIES[4]
        params = query["bind"]({"year": 4})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0


class TestQuery6ResearchProjects:
    """Tests for Query 6: Research Projects by Status."""
    
    def test_query_6_active_status(self, demo_connection):
        """TC-Q-010: Query 6 returns active research projects."""
        query = queries.QUERIES[5]
        assert query["id"] == 6
        
        params = query["bind"]({"status": "Active"})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
    
    def test_query_6_completed_status(self, demo_connection):
        """TC-Q-011: Query 6 returns completed research projects."""
        query = queries.QUERIES[5]
        params = query["bind"]({"status": "Completed"})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0


class TestQuery7HighPerformers:
    """Tests for Query 7: High-Performing Students."""
    
    def test_query_7_threshold_75(self, demo_connection):
        """TC-Q-012: Query 7 returns students with avg >= 75%."""
        query = queries.QUERIES[6]
        assert query["id"] == 7
        
        params = query["bind"]({"threshold": 75})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
        assert "Average %" in result.columns
    
    def test_query_7_threshold_90(self, demo_connection):
        """TC-Q-013: Query 7 returns students with avg >= 90%."""
        query = queries.QUERIES[6]
        params = query["bind"]({"threshold": 90})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
        # All results should meet threshold
        assert all(result["Average %"] >= 90)
    
    def test_query_7_ordered_descending(self, demo_connection):
        """Query 7 orders results by average grade descending."""
        query = queries.QUERIES[6]
        params = query["bind"]({"threshold": 75})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        # Verify descending order
        averages = result["Average %"].tolist()
        assert averages == sorted(averages, reverse=True)


class TestQuery8EnrollmentCounts:
    """Tests for Query 8: Course Enrollment Counts."""
    
    def test_query_8_no_params(self, demo_connection):
        """TC-Q-014: Query 8 returns enrollment counts for all courses."""
        query = queries.QUERIES[7]
        assert query["id"] == 8
        assert query["params"] == []  # No parameters
        
        params = query["bind"]({})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
        assert "Course Code" in result.columns
        assert "Enrolled" in result.columns


class TestQuery9PublicationsSince:
    """Tests for Query 9: Publications Since a Date."""
    
    def test_query_9_valid_date(self, demo_connection):
        """TC-Q-015: Query 9 returns publications on or after date."""
        query = queries.QUERIES[8]
        assert query["id"] == 9
        
        params = query["bind"]({"since": "2023-01-01"})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)


class TestQuery10StaffByEmployment:
    """Tests for Query 10: Staff by Employment Type."""
    
    def test_query_10_full_time(self, demo_connection):
        """TC-Q-016: Query 10 returns full-time non-academic staff."""
        query = queries.QUERIES[9]
        assert query["id"] == 10
        
        params = query["bind"]({"etype": "Full-Time"})
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert len(result) > 0
        assert "Staff ID" in result.columns


class TestQueryBindingFunctions:
    """Tests for query binding lambdas."""
    
    def test_query_bind_returns_correct_format(self):
        """Each query bind() returns tuple or dict as needed by SQL."""
        for query in queries.QUERIES:
            test_params = {p["key"]: (1 if p["kind"] != "select" else "option1") 
                          for p in query["params"]}
            result = query["bind"](test_params)
            # Should return tuple, dict, or empty tuple
            assert isinstance(result, (tuple, dict))
    
    def test_query_with_optional_params(self):
        """Query 1 bind handles optional department parameter."""
        query = queries.QUERIES[0]
        
        # With value
        result1 = query["bind"]({"dept": 1})
        assert result1 == {"dept": 1}
        
        # With None
        result2 = query["bind"]({"dept": None})
        assert result2 == {"dept": None}


class TestQueryEdgeCases:
    """Edge case tests for queries."""
    
    def test_empty_parameter_dict(self, demo_connection):
        """Query 8 handles empty parameter dict correctly."""
        query = queries.QUERIES[7]  # No params query
        params = query["bind"]({})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_sql_injection_safety(self, demo_connection):
        """Queries use parameterized statements (safe from injection)."""
        query = queries.QUERIES[1]  # Course enrollment
        
        # Try injection in parameter
        malicious = "CS101'; DROP TABLE STUDENT; --"
        params = query["bind"]({"course": malicious})
        
        with patch('src.urms.database.get_connection', return_value=demo_connection):
            result = database.run_query(query["sql"], params)
        
        # Should not execute injection, just find no results
        assert isinstance(result, pd.DataFrame)
        # STUDENT table should still exist
        check = database.run_query("SELECT COUNT(*) FROM STUDENT")
        assert check.iloc[0, 0] == 12
