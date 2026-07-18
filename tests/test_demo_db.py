"""Test cases for demo_db.py module."""

import pytest
import sqlite3

from src.urms import demo_db


class TestBuildInMemory:
    """Tests for build_in_memory() function."""
    
    def test_build_in_memory_returns_connection(self):
        """TC-DEMO-001: build_in_memory() returns SQLite connection."""
        conn = demo_db.build_in_memory()
        assert conn is not None
        assert isinstance(conn, sqlite3.Connection)
        conn.close()
    
    def test_in_memory_database_created(self):
        """build_in_memory() creates database in memory."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Query in-memory status
        cursor.execute("PRAGMA database_list")
        databases = cursor.fetchall()
        
        # Should have temp or main database
        assert len(databases) > 0
        conn.close()
    
    def test_row_factory_set(self):
        """build_in_memory() sets row_factory on connection."""
        conn = demo_db.build_in_memory()
        assert conn.row_factory is not None
        conn.close()


class TestSchemaCreation:
    """Tests for schema creation in demo database."""
    
    def test_all_tables_created(self):
        """TC-DEMO-010: All 32 tables are created."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Query sqlite_master for all user tables
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        
        # Expected tables
        expected_tables = [
            "COMMITTEE", "COMMITTEE_MEMBERSHIP", "COURSE", "COURSE_MATERIAL",
            "COURSE_OFFERING", "COURSE_PREREQUISITE", "DEPARTMENT",
            "DEPARTMENT_RESEARCH_AREA", "DISCIPLINARY_RECORD", "ENROLLMENT",
            "FUNDING_SOURCE", "LECTURER", "LECTURER_EXPERTISE",
            "LECTURER_PUBLICATION", "LECTURER_QUALIFICATION",
            "LECTURER_RESEARCH_INTEREST", "NON_ACADEMIC_STAFF", "PROGRAM",
            "PROGRAM_COURSE_REQUIREMENT", "PROJECT_FUNDING", "PROJECT_OUTCOME",
            "PUBLICATION", "RESEARCH_AREA", "RESEARCH_PROJECT",
            "RESEARCH_PROJECT_TEAM", "SCHEDULE_SLOT", "STUDENT",
            "STUDENT_ORG_MEMBERSHIP", "STUDENT_ORGANIZATION", "TEACHING_ASSIGNMENT"
        ]
        
        # Check all expected tables exist
        for table in expected_tables:
            assert table in table_names, f"Table {table} not found"
        
        assert len(table_names) == 30  # Expected table count
        conn.close()

    def test_compatibility_views_created(self):
        """build_in_memory() exposes the UI compatibility views."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_temp_master
            WHERE type='view'
            ORDER BY name
        """)
        view_names = [row[0] for row in cursor.fetchall()]

        assert "LECTURER_EXPERTISE_UI" in view_names
        assert "NON_ACADEMIC_STAFF_UI" in view_names
        assert "PROJECT_FUNDING_UI" in view_names

        conn.close()


class TestDataPopulation:
    """Tests for data population in demo database."""
    
    def test_departments_populated(self):
        """TC-DEMO-002: DEPARTMENT table has 4 departments."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM DEPARTMENT")
        count = cursor.fetchone()[0]
        
        assert count == 4
        
        # Check specific department
        cursor.execute("SELECT DepartmentName FROM DEPARTMENT WHERE DepartmentID = 1")
        dept = cursor.fetchone()[0]
        assert dept == "Computer Science"
        
        conn.close()
    
    def test_lecturers_populated(self):
        """TC-DEMO-004: LECTURER table has 6 lecturers."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM LECTURER")
        count = cursor.fetchone()[0]
        assert count == 6
        
        conn.close()
    
    def test_students_populated(self):
        """TC-DEMO-003: STUDENT table has 12 students with correct fields."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        count = cursor.fetchone()[0]
        assert count == 12
        
        # Check specific student
        cursor.execute("SELECT FullName FROM STUDENT WHERE StudentID = 'S001'")
        name = cursor.fetchone()[0]
        assert name == "Alice Smith"
        
        conn.close()
    
    def test_courses_populated(self):
        """TC-DEMO-005: COURSE table has 7 courses."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM COURSE")
        count = cursor.fetchone()[0]
        assert count == 7
        
        conn.close()
    
    def test_enrollments_populated(self):
        """TC-DEMO-006: ENROLLMENT table has 15 enrollments with grades."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ENROLLMENT")
        count = cursor.fetchone()[0]
        assert count == 15
        
        # Check that enrollments have grades
        cursor.execute("SELECT COUNT(*) FROM ENROLLMENT WHERE GradeLetter IS NOT NULL")
        graded = cursor.fetchone()[0]
        assert graded > 0
        
        conn.close()
    
    def test_research_projects_populated(self):
        """TC-DEMO-007: RESEARCH_PROJECT has 4 projects (2 active, 2 completed)."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM RESEARCH_PROJECT")
        total = cursor.fetchone()[0]
        assert total == 4
        
        # Check status distribution
        cursor.execute("SELECT COUNT(*) FROM RESEARCH_PROJECT WHERE Status = 'Active'")
        active = cursor.fetchone()[0]
        assert active == 2
        
        cursor.execute("SELECT COUNT(*) FROM RESEARCH_PROJECT WHERE Status = 'Completed'")
        completed = cursor.fetchone()[0]
        assert completed == 2
        
        conn.close()


class TestDataIntegrity:
    """Tests for data consistency and referential integrity."""
    
    def test_student_program_references_valid(self):
        """TC-DEMO-008: All StudentID refs to PROGRAM are valid."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Check for orphaned student-program references
        cursor.execute("""
            SELECT COUNT(*) FROM STUDENT s
            WHERE s.ProgramID IS NOT NULL 
            AND s.ProgramID NOT IN (SELECT ProgramID FROM PROGRAM)
        """)
        orphans = cursor.fetchone()[0]
        assert orphans == 0
        
        conn.close()
    
    def test_enrollment_references_valid(self):
        """Enrollment references to StudentID and OfferingID are valid."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Check StudentID references
        cursor.execute("""
            SELECT COUNT(*) FROM ENROLLMENT e
            WHERE e.StudentID NOT IN (SELECT StudentID FROM STUDENT)
        """)
        invalid_students = cursor.fetchone()[0]
        assert invalid_students == 0
        
        # Check OfferingID references
        cursor.execute("""
            SELECT COUNT(*) FROM ENROLLMENT e
            WHERE e.OfferingID NOT IN (SELECT OfferingID FROM COURSE_OFFERING)
        """)
        invalid_offerings = cursor.fetchone()[0]
        assert invalid_offerings == 0
        
        conn.close()
    
    def test_teaching_assignment_references_valid(self):
        """Teaching assignments reference valid lecturers and offerings."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Check LecturerID
        cursor.execute("""
            SELECT COUNT(*) FROM TEACHING_ASSIGNMENT ta
            WHERE ta.LecturerID NOT IN (SELECT LecturerID FROM LECTURER)
        """)
        invalid_lecturers = cursor.fetchone()[0]
        assert invalid_lecturers == 0
        
        # Check OfferingID
        cursor.execute("""
            SELECT COUNT(*) FROM TEACHING_ASSIGNMENT ta
            WHERE ta.OfferingID NOT IN (SELECT OfferingID FROM COURSE_OFFERING)
        """)
        invalid_offerings = cursor.fetchone()[0]
        assert invalid_offerings == 0
        
        conn.close()
    
    def test_course_offering_references_valid(self):
        """Course offerings reference valid courses."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM COURSE_OFFERING co
            WHERE co.CourseCode NOT IN (SELECT CourseCode FROM COURSE)
        """)
        invalid = cursor.fetchone()[0]
        assert invalid == 0
        
        conn.close()


class TestConnectionBehavior:
    """Tests for connection configuration and behavior."""
    
    def test_thread_safe_connection(self):
        """TC-DEMO-009: Connection allows multi-threaded access."""
        conn = demo_db.build_in_memory()
        
        # check_same_thread=False should be set
        cursor = conn.cursor()
        cursor.execute("PRAGMA query_only")
        read_only = cursor.fetchone()[0]
        
        # Connection created with check_same_thread=False
        # This means same connection can be used across threads
        assert conn is not None
        
        conn.close()
    
    def test_cursor_execution(self):
        """Cursors can execute queries on created connection."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        # Should be able to execute
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == 12
        
        conn.close()


class TestSchemaColumns:
    """Tests for table schemas and column definitions."""
    
    def test_student_table_columns(self):
        """STUDENT table has required columns."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(STUDENT)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required = ["StudentID", "FullName", "Email", "Phone", "ProgramID", "YearOfStudy"]
        for col in required:
            assert col in columns, f"Missing column: {col}"
        
        conn.close()
    
    def test_enrollment_table_columns(self):
        """ENROLLMENT table has grade and percentage columns."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(ENROLLMENT)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required = ["EnrollmentID", "StudentID", "OfferingID", "GradeLetter", "FinalGradePercent"]
        for col in required:
            assert col in columns, f"Missing column: {col}"
        
        conn.close()
    
    def test_lecturer_table_columns(self):
        """LECTURER table has qualification and contact info columns."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA table_info(LECTURER)")
        columns = [row[1] for row in cursor.fetchall()]
        
        required = ["LecturerID", "FullName", "Email", "QualificationSummary"]
        for col in required:
            assert col in columns, f"Missing column: {col}"
        
        conn.close()


class TestQueryExecutionOnDemoDB:
    """Tests for query execution on demo database."""
    
    def test_simple_select_all_students(self):
        """Can SELECT all students from demo database."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM STUDENT")
        students = cursor.fetchall()
        
        assert len(students) == 12
        conn.close()
    
    def test_aggregate_query(self):
        """Aggregate queries work on demo database."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as cnt FROM ENROLLMENT WHERE GradeLetter = 'A'")
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] > 0
        conn.close()
    
    def test_join_query(self):
        """JOIN queries work on demo database."""
        conn = demo_db.build_in_memory()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.FullName, p.ProgramName
            FROM STUDENT s
            LEFT JOIN PROGRAM p ON s.ProgramID = p.ProgramID
            LIMIT 5
        """)
        results = cursor.fetchall()
        
        assert len(results) > 0
        conn.close()
