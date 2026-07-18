"""
Database access layer for the Streamlit front end.

Every page talks to the database through this module.  The Streamlit interface
was originally built against a compact demo schema, while the backend SQL file
uses the final normalised schema. To merge the two cleanly, real backend
connections get temporary compatibility views such as ``STUDENT`` and
``COURSE`` that map onto backend tables such as ``students`` and ``courses``.

Connection strategy
-------------------
1. If ``database/university.db`` exists, connect to it read-only and install the
   compatibility views for the front end.
2. Otherwise fall back to the in-memory demo database from ``demo_db.py`` so the
   interface can still be demonstrated without a committed database file.

The active source is exposed via :func:`data_source_label` so the UI can show
which database it is using.
"""

from __future__ import annotations

from pathlib import Path
import sqlite3

import pandas as pd

try:
    import streamlit as st
except ModuleNotFoundError:  # pragma: no cover - used only by non-Streamlit checks
    class _StreamlitFallback:
        @staticmethod
        def cache_resource(*_args, **_kwargs):
            def decorator(func):
                return func

            return decorator

    st = _StreamlitFallback()

from . import demo_db

# database/university.db sits two levels up from this file: src/urms/ -> repo/database
_REPO_ROOT = Path(__file__).resolve().parents[2]
_REAL_DB_PATH = _REPO_ROOT / "database" / "university.db"
_BACKEND_SCHEMA_PATH = _REPO_ROOT / "database" / "UniversityRecordManagementDatabase.sql"
_BACKEND_DUMMY_DATA_PATH = _REPO_ROOT / "database" / "Dummy Data.sql"


@st.cache_resource(show_spinner=False)
def get_connection():
    """Return a cached SQLite connection (real DB if present, else demo DB)."""
    if _REAL_DB_PATH.exists():
        conn = sqlite3.connect(f"file:{_REAL_DB_PATH}?mode=ro", uri=True, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        install_backend_compatibility_views(conn)
        return conn
    conn = demo_db.build_in_memory()
    install_demo_compatibility_views(conn)
    return conn


def build_backend_schema_connection(load_dummy_data: bool = True) -> sqlite3.Connection:
    """Build an in-memory connection from the backend SQL schema for checks.

    The repository does not currently commit ``database/university.db``. This
    helper lets tests and developers validate that the front end can query the
    backend schema once it is turned into a SQLite database.
    """

    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(_BACKEND_SCHEMA_PATH.read_text(encoding="utf-8"))
    if load_dummy_data and _BACKEND_DUMMY_DATA_PATH.exists():
        conn.executescript(_BACKEND_DUMMY_DATA_PATH.read_text(encoding="utf-8"))
    install_backend_compatibility_views(conn)
    return conn


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


def install_backend_compatibility_views(conn: sqlite3.Connection) -> None:
    """Expose the backend schema through the names used by the front end."""

    if not _has_relation(conn, "students"):
        return

    conn.executescript(
        """
        CREATE TEMP VIEW IF NOT EXISTS DEPARTMENT AS
        SELECT
            d.department_id AS DepartmentID,
            d.department_name AS DepartmentName,
            COALESCE(f.faculty_name, '') AS Faculty,
            d.office_location AS OfficeLocation
        FROM departments d
        LEFT JOIN faculties f ON f.faculty_id = d.faculty_id;

        CREATE TEMP VIEW IF NOT EXISTS RESEARCH_AREA AS
        SELECT
            research_area_id AS ResearchAreaID,
            area_name AS AreaName,
            description AS Description
        FROM research_areas;

        CREATE TEMP VIEW IF NOT EXISTS DEPARTMENT_RESEARCH_AREA AS
        SELECT
            department_id AS DepartmentID,
            research_area_id AS ResearchAreaID
        FROM department_research_areas;

        CREATE TEMP VIEW IF NOT EXISTS PROGRAM AS
        SELECT
            program_id AS ProgramID,
            program_name AS ProgramName,
            department_id AS DepartmentID,
            degree_awarded AS DegreeAwarded,
            duration_years AS DurationYears,
            enrollment_details AS EnrollmentDetails
        FROM programs;

        CREATE TEMP VIEW IF NOT EXISTS LECTURER AS
        SELECT
            l.lecturer_number AS LecturerID,
            l.first_name || ' ' || l.last_name AS FullName,
            l.department_id AS DepartmentID,
            l.email AS Email,
            l.phone AS Phone,
            COALESCE(d.office_location, '') AS Office,
            COALESCE(
                (
                    SELECT GROUP_CONCAT(lq.qualification_name, ', ')
                    FROM lecturer_qualifications lq
                    WHERE lq.lecturer_id = l.lecturer_id
                ),
                ''
            ) AS QualificationSummary,
            l.course_load_hours AS CourseLoad,
            l.employment_status AS EmploymentStatus
        FROM lecturers l
        LEFT JOIN departments d ON d.department_id = l.department_id;

        CREATE TEMP VIEW IF NOT EXISTS LECTURER_QUALIFICATION AS
        SELECT
            l.lecturer_number AS LecturerID,
            q.qualification_name AS DegreeName,
            q.institution AS Institution,
            q.year_awarded AS AwardYear
        FROM lecturer_qualifications q
        JOIN lecturers l ON l.lecturer_id = q.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS LECTURER_RESEARCH_INTEREST AS
        SELECT
            l.lecturer_number AS LecturerID,
            i.research_area_id AS ResearchAreaID
        FROM lecturer_research_interests i
        JOIN lecturers l ON l.lecturer_id = i.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS LECTURER_EXPERTISE_UI AS
        SELECT
            l.lecturer_number AS LecturerID,
            e.research_area_id AS ResearchAreaID,
            e.expertise_level AS ExpertiseLevel
        FROM lecturer_expertise e
        JOIN lecturers l ON l.lecturer_id = e.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS PUBLICATION AS
        SELECT
            publication_id AS PublicationID,
            title AS Title,
            venue AS Venue,
            COALESCE(publication_date, printf('%04d-01-01', publication_year)) AS PublicationDate,
            publication_type AS PublicationType,
            doi AS Doi
        FROM publications;

        CREATE TEMP VIEW IF NOT EXISTS LECTURER_PUBLICATION AS
        SELECT
            l.lecturer_number AS LecturerID,
            lp.publication_id AS PublicationID,
            lp.author_order AS AuthorOrder
        FROM lecturer_publications lp
        JOIN lecturers l ON l.lecturer_id = lp.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS COMMITTEE AS
        SELECT
            committee_id AS CommitteeID,
            committee_name AS CommitteeName,
            department_id AS DepartmentID,
            purpose AS Purpose
        FROM committees;

        CREATE TEMP VIEW IF NOT EXISTS COMMITTEE_MEMBERSHIP AS
        SELECT
            l.lecturer_number AS LecturerID,
            cm.committee_id AS CommitteeID,
            cm.role_title AS RoleTitle,
            cm.start_date AS StartDate,
            cm.end_date AS EndDate
        FROM committee_memberships cm
        JOIN lecturers l ON l.lecturer_id = cm.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS STUDENT AS
        SELECT
            s.student_number AS StudentID,
            s.first_name || ' ' || s.last_name AS FullName,
            s.date_of_birth AS DateOfBirth,
            (
                SELECT sc.contact_value
                FROM student_contacts sc
                WHERE sc.student_id = s.student_id AND sc.contact_type = 'Email'
                ORDER BY sc.is_primary DESC, sc.contact_id
                LIMIT 1
            ) AS Email,
            (
                SELECT sc.contact_value
                FROM student_contacts sc
                WHERE sc.student_id = s.student_id AND sc.contact_type = 'Phone'
                ORDER BY sc.is_primary DESC, sc.contact_id
                LIMIT 1
            ) AS Phone,
            s.program_id AS ProgramID,
            s.year_of_study AS YearOfStudy,
            s.graduation_status AS GraduationStatus,
            (
                SELECT l.lecturer_number
                FROM student_advisors sa
                JOIN lecturers l ON l.lecturer_id = sa.lecturer_id
                WHERE sa.student_id = s.student_id
                ORDER BY sa.end_date IS NULL DESC, sa.start_date DESC
                LIMIT 1
            ) AS AdvisorLecturerID
        FROM students s;

        CREATE TEMP VIEW IF NOT EXISTS STUDENT_ORGANIZATION AS
        SELECT
            organization_id AS OrgID,
            organization_name AS OrgName,
            department_id AS DepartmentID,
            description AS Description
        FROM student_organizations;

        CREATE TEMP VIEW IF NOT EXISTS STUDENT_ORG_MEMBERSHIP AS
        SELECT
            s.student_number AS StudentID,
            r.organization_id AS OrgID,
            r.role_title AS RoleTitle,
            r.registered_date AS RegisteredDate,
            r.active AS Active
        FROM student_organization_registrations r
        JOIN students s ON s.student_id = r.student_id;

        CREATE TEMP VIEW IF NOT EXISTS DISCIPLINARY_RECORD AS
        SELECT
            d.disciplinary_record_id AS RecordID,
            s.student_number AS StudentID,
            d.incident_date AS IncidentDate,
            d.description AS Description,
            d.status AS Status,
            d.action_taken AS ActionTaken
        FROM disciplinary_records d
        JOIN students s ON s.student_id = d.student_id;

        CREATE TEMP VIEW IF NOT EXISTS COURSE AS
        SELECT
            course_code AS CourseCode,
            course_name AS CourseName,
            department_id AS DepartmentID,
            CASE WHEN level <= 4 THEN 'Undergraduate' ELSE 'Postgraduate' END AS Level,
            credits AS Credits,
            description AS Description
        FROM courses;

        CREATE TEMP VIEW IF NOT EXISTS COURSE_PREREQUISITE AS
        SELECT
            c.course_code AS CourseCode,
            p.course_code AS PrereqCourseCode
        FROM course_prerequisites cp
        JOIN courses c ON c.course_id = cp.course_id
        JOIN courses p ON p.course_id = cp.prerequisite_course_id;

        CREATE TEMP VIEW IF NOT EXISTS COURSE_OFFERING AS
        SELECT
            co.offering_id AS OfferingID,
            c.course_code AS CourseCode,
            CAST(s.academic_year AS TEXT) AS AcademicYear,
            s.term AS Semester,
            co.schedule AS Schedule,
            co.capacity AS Capacity
        FROM course_offerings co
        JOIN courses c ON c.course_id = co.course_id
        JOIN semesters s ON s.semester_id = co.semester_id;

        CREATE TEMP VIEW IF NOT EXISTS SCHEDULE_SLOT AS
        SELECT
            offering_id AS OfferingID,
            schedule AS DayOfWeek,
            '' AS StartTime,
            '' AS EndTime,
            '' AS Room
        FROM course_offerings;

        CREATE TEMP VIEW IF NOT EXISTS COURSE_MATERIAL AS
        SELECT
            co.offering_id AS OfferingID,
            cm.title AS Title,
            cm.material_type AS MaterialType,
            cm.material_url AS MaterialUrl
        FROM course_materials cm
        JOIN course_offerings co ON co.course_id = cm.course_id;

        CREATE TEMP VIEW IF NOT EXISTS TEACHING_ASSIGNMENT AS
        SELECT
            l.lecturer_number AS LecturerID,
            ta.offering_id AS OfferingID,
            CASE
                WHEN lower(ta.teaching_role) LIKE '%lead%' THEN 'Primary'
                ELSE ta.teaching_role
            END AS TeachingRole
        FROM teaching_assignments ta
        JOIN lecturers l ON l.lecturer_id = ta.lecturer_id;

        CREATE TEMP VIEW IF NOT EXISTS ENROLLMENT AS
        SELECT
            e.enrollment_id AS EnrollmentID,
            s.student_number AS StudentID,
            e.offering_id AS OfferingID,
            CASE
                WHEN e.final_grade_percent >= 70 THEN 'A'
                WHEN e.final_grade_percent >= 60 THEN 'B'
                WHEN e.final_grade_percent >= 50 THEN 'C'
                WHEN e.final_grade_percent IS NULL THEN NULL
                ELSE 'F'
            END AS GradeLetter,
            e.final_grade_percent AS FinalGradePercent,
            e.enrollment_status AS EnrollmentStatus
        FROM enrollments e
        JOIN students s ON s.student_id = e.student_id;

        CREATE TEMP VIEW IF NOT EXISTS NON_ACADEMIC_STAFF_UI AS
        SELECT
            st.staff_number AS StaffID,
            st.first_name || ' ' || st.last_name AS FullName,
            st.job_title AS JobTitle,
            st.department_id AS DepartmentID,
            CASE st.employment_type
                WHEN 'Full-time' THEN 'Full-Time'
                WHEN 'Part-time' THEN 'Part-Time'
                ELSE st.employment_type
            END AS EmploymentType,
            COALESCE(
                (
                    SELECT sc.contract_details
                    FROM staff_contracts sc
                    WHERE sc.staff_id = st.staff_id
                    ORDER BY sc.contract_start_date DESC
                    LIMIT 1
                ),
                CASE WHEN st.employment_type = 'Contract' THEN 'Contract' ELSE 'Permanent' END
            ) AS ContractType,
            st.email AS Email,
            st.phone AS Phone
        FROM main.non_academic_staff st;

        CREATE TEMP VIEW IF NOT EXISTS PROGRAM_COURSE_REQUIREMENT AS
        SELECT
            pcr.program_id AS ProgramID,
            c.course_code AS CourseCode,
            c.credits AS Credits,
            pcr.requirement_type AS Semester,
            pcr.recommended_year AS RecommendedYear,
            pcr.minimum_grade_percent AS MinimumGradePercent
        FROM program_course_requirements pcr
        JOIN courses c ON c.course_id = pcr.course_id;

        CREATE TEMP VIEW IF NOT EXISTS RESEARCH_PROJECT AS
        SELECT
            rp.project_id AS ProjectID,
            rp.project_title AS ProjectTitle,
            l.lecturer_number AS PrincipalInvestigatorID,
            COALESCE(rg.department_id, l.department_id) AS DepartmentID,
            rp.project_status AS Status,
            rp.start_date AS StartDate,
            rp.end_date AS EndDate
        FROM research_projects rp
        JOIN lecturers l ON l.lecturer_id = rp.principal_investigator_id
        LEFT JOIN research_groups rg ON rg.research_group_id = rp.research_group_id;

        CREATE TEMP VIEW IF NOT EXISTS FUNDING_SOURCE AS
        SELECT
            funding_source_id AS FundingSourceID,
            source_name AS SourceName,
            source_type AS SourceType
        FROM funding_sources;

        CREATE TEMP VIEW IF NOT EXISTS PROJECT_FUNDING_UI AS
        SELECT
            project_id AS ProjectID,
            funding_source_id AS FundingSourceID,
            'MUR ' AS Currency,
            amount AS AmountAwarded,
            grant_reference AS GrantReference
        FROM project_funding;

        CREATE TEMP VIEW IF NOT EXISTS RESEARCH_PROJECT_TEAM AS
        SELECT
            ptm.project_id AS ProjectID,
            COALESCE(
                stu.first_name || ' ' || stu.last_name,
                lec.first_name || ' ' || lec.last_name,
                staff.first_name || ' ' || staff.last_name
            ) AS MemberName,
            ptm.member_role AS ProjectRole,
            COALESCE(stu_dept.department_name, lec_dept.department_name, staff_dept.department_name, '') AS DepartmentName
        FROM project_team_members ptm
        LEFT JOIN students stu ON stu.student_id = ptm.student_id
        LEFT JOIN programs prog ON prog.program_id = stu.program_id
        LEFT JOIN departments stu_dept ON stu_dept.department_id = prog.department_id
        LEFT JOIN lecturers lec ON lec.lecturer_id = ptm.lecturer_id
        LEFT JOIN departments lec_dept ON lec_dept.department_id = lec.department_id
        LEFT JOIN non_academic_staff staff ON staff.staff_id = ptm.staff_id
        LEFT JOIN departments staff_dept ON staff_dept.department_id = staff.department_id;

        CREATE TEMP VIEW IF NOT EXISTS PROJECT_OUTCOME AS
        SELECT
            project_id AS ProjectID,
            description AS Description,
            outcome_type AS OutcomeType,
            outcome_date AS OutcomeDate
        FROM project_outcomes;
        """
    )


def install_demo_compatibility_views(conn: sqlite3.Connection) -> None:
    """Expose aliases that keep demo and backend query names consistent."""

    aliases = {
        "NON_ACADEMIC_STAFF_UI": "NON_ACADEMIC_STAFF",
        "LECTURER_EXPERTISE_UI": "LECTURER_EXPERTISE",
        "PROJECT_FUNDING_UI": "PROJECT_FUNDING",
    }
    for alias, source in aliases.items():
        if not _has_relation(conn, alias):
            conn.execute(f"CREATE TEMP VIEW {alias} AS SELECT * FROM {source}")


def _has_relation(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE name = ? AND type IN ('table', 'view')
        UNION ALL
        SELECT 1
        FROM sqlite_temp_master
        WHERE name = ? AND type IN ('table', 'view')
        LIMIT 1
        """,
        (name, name),
    ).fetchone()
    return row is not None
