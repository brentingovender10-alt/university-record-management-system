"""
In-memory demo database for standalone runs of the front end.

When ``database/university.db`` (the real database to be produced from the back end) is not present, ``database.py`` builds this illustrative SQLite
database in memory so the interface can always run and be demonstrated on its
own.  The schema and column names follow the group-validated logical ERD.

The data here is small, fictional and for demonstration only.
"""

from __future__ import annotations

import sqlite3

_SCHEMA = """
CREATE TABLE DEPARTMENT (
    DepartmentID   INTEGER PRIMARY KEY,
    DepartmentName TEXT NOT NULL,
    Faculty        TEXT NOT NULL
);

CREATE TABLE RESEARCH_AREA (
    ResearchAreaID INTEGER PRIMARY KEY,
    AreaName       TEXT NOT NULL
);

CREATE TABLE DEPARTMENT_RESEARCH_AREA (
    DepartmentID   INTEGER,
    ResearchAreaID INTEGER
);

CREATE TABLE PROGRAM (
    ProgramID     INTEGER PRIMARY KEY,
    ProgramName   TEXT NOT NULL,
    DepartmentID  INTEGER,
    DegreeAwarded TEXT,
    DurationYears INTEGER
);

CREATE TABLE LECTURER (
    LecturerID           TEXT PRIMARY KEY,
    FullName             TEXT NOT NULL,
    DepartmentID         INTEGER,
    Email                TEXT,
    Phone                TEXT,
    Office               TEXT,
    QualificationSummary TEXT,
    CourseLoad           INTEGER
);

CREATE TABLE LECTURER_QUALIFICATION (
    LecturerID  TEXT,
    DegreeName  TEXT,
    Institution TEXT,
    AwardYear   INTEGER
);

CREATE TABLE LECTURER_RESEARCH_INTEREST (
    LecturerID     TEXT,
    ResearchAreaID INTEGER
);

CREATE TABLE LECTURER_EXPERTISE (
    LecturerID     TEXT,
    ResearchAreaID INTEGER
);

CREATE TABLE PUBLICATION (
    PublicationID   INTEGER PRIMARY KEY,
    Title           TEXT,
    Venue           TEXT,
    PublicationDate TEXT
);

CREATE TABLE LECTURER_PUBLICATION (
    LecturerID    TEXT,
    PublicationID INTEGER
);

CREATE TABLE COMMITTEE (
    CommitteeID   INTEGER PRIMARY KEY,
    CommitteeName TEXT
);

CREATE TABLE COMMITTEE_MEMBERSHIP (
    LecturerID  TEXT,
    CommitteeID INTEGER
);

CREATE TABLE STUDENT (
    StudentID          TEXT PRIMARY KEY,
    FullName           TEXT NOT NULL,
    DateOfBirth        TEXT,
    Email              TEXT,
    Phone              TEXT,
    ProgramID          INTEGER,
    YearOfStudy        INTEGER,
    GraduationStatus   TEXT,
    AdvisorLecturerID  TEXT
);

CREATE TABLE STUDENT_ORGANIZATION (
    OrgID   INTEGER PRIMARY KEY,
    OrgName TEXT
);

CREATE TABLE STUDENT_ORG_MEMBERSHIP (
    StudentID TEXT,
    OrgID     INTEGER
);

CREATE TABLE DISCIPLINARY_RECORD (
    RecordID     INTEGER PRIMARY KEY,
    StudentID    TEXT,
    IncidentDate TEXT,
    Description  TEXT,
    Status       TEXT
);

CREATE TABLE COURSE (
    CourseCode   TEXT PRIMARY KEY,
    CourseName   TEXT NOT NULL,
    DepartmentID INTEGER,
    Level        TEXT,
    Credits      INTEGER,
    Description  TEXT
);

CREATE TABLE COURSE_PREREQUISITE (
    CourseCode       TEXT,
    PrereqCourseCode TEXT
);

CREATE TABLE COURSE_OFFERING (
    OfferingID   INTEGER PRIMARY KEY,
    CourseCode   TEXT,
    AcademicYear TEXT,
    Semester     TEXT
);

CREATE TABLE SCHEDULE_SLOT (
    OfferingID INTEGER,
    DayOfWeek  TEXT,
    StartTime  TEXT,
    EndTime    TEXT,
    Room       TEXT
);

CREATE TABLE COURSE_MATERIAL (
    OfferingID INTEGER,
    Title      TEXT
);

CREATE TABLE TEACHING_ASSIGNMENT (
    LecturerID   TEXT,
    OfferingID   INTEGER,
    TeachingRole TEXT
);

CREATE TABLE ENROLLMENT (
    EnrollmentID      INTEGER PRIMARY KEY,
    StudentID         TEXT,
    OfferingID        INTEGER,
    GradeLetter       TEXT,
    FinalGradePercent REAL
);

CREATE TABLE NON_ACADEMIC_STAFF (
    StaffID        TEXT PRIMARY KEY,
    FullName       TEXT NOT NULL,
    JobTitle       TEXT,
    DepartmentID   INTEGER,
    EmploymentType TEXT,
    ContractType   TEXT
);

CREATE TABLE PROGRAM_COURSE_REQUIREMENT (
    ProgramID       INTEGER,
    CourseCode      TEXT,
    Credits         INTEGER,
    Semester        TEXT,
    RecommendedYear INTEGER
);

CREATE TABLE RESEARCH_PROJECT (
    ProjectID                INTEGER PRIMARY KEY,
    ProjectTitle             TEXT,
    PrincipalInvestigatorID  TEXT,
    DepartmentID             INTEGER,
    Status                   TEXT,
    StartDate                TEXT,
    EndDate                  TEXT
);

CREATE TABLE FUNDING_SOURCE (
    FundingSourceID INTEGER PRIMARY KEY,
    SourceName      TEXT,
    SourceType      TEXT
);

CREATE TABLE PROJECT_FUNDING (
    ProjectID       INTEGER,
    FundingSourceID INTEGER,
    Currency        TEXT,
    AmountAwarded   INTEGER
);

CREATE TABLE RESEARCH_PROJECT_TEAM (
    ProjectID      INTEGER,
    MemberName     TEXT,
    ProjectRole    TEXT,
    DepartmentName TEXT
);

CREATE TABLE PROJECT_OUTCOME (
    ProjectID   INTEGER,
    Description TEXT
);
"""

# --- Reference data ---------------------------------------------------------

_DEPARTMENTS = [
    (1, "Computer Science", "Faculty of Science and Engineering"),
    (2, "Electrical Engineering", "Faculty of Science and Engineering"),
    (3, "Business Management", "Faculty of Business"),
    (4, "Mathematics", "Faculty of Science and Engineering"),
]

_RESEARCH_AREAS = [
    (1, "Artificial Intelligence"),
    (2, "Cybersecurity"),
    (3, "Power Systems"),
    (4, "Data Science"),
    (5, "Finance"),
    (6, "Applied Mathematics"),
]

_DEPARTMENT_RESEARCH_AREAS = [
    (1, 1), (1, 2), (1, 4),
    (2, 3),
    (3, 5),
    (4, 6),
]

_PROGRAMS = [
    (1, "BSc Computer Science", 1, "Bachelor of Science", 3),
    (2, "MSc Data Science", 1, "Master of Science", 2),
    (3, "BEng Electrical Engineering", 2, "Bachelor of Engineering", 4),
    (4, "BBA Business Administration", 3, "Bachelor of Business Administration", 3),
    (5, "MBA", 3, "Master of Business Administration", 2),
    (6, "BSc Mathematics", 4, "Bachelor of Science", 3),
]

_LECTURERS = [
    ("L001", "Dr. Alan Turing", 1, "a.turing@uni.edu", "+44 20 7000 0001", "CS-201",
     "PhD Computer Science", 3),
    ("L002", "Dr. Grace Hopper", 1, "g.hopper@uni.edu", "+44 20 7000 0002", "CS-204",
     "PhD Computer Science", 2),
    ("L003", "Dr. Nikola Volt", 2, "n.volt@uni.edu", "+44 20 7000 0003", "EE-110",
     "PhD Electrical Engineering", 3),
    ("L004", "Prof. Ada Ledger", 3, "a.ledger@uni.edu", "+44 20 7000 0004", "BM-305",
     "PhD Finance", 2),
    ("L005", "Dr. Carl Gauss", 4, "c.gauss@uni.edu", "+44 20 7000 0005", "MA-014",
     "PhD Mathematics", 3),
    ("L006", "Dr. Marie Secure", 1, "m.secure@uni.edu", "+44 20 7000 0006", "CS-210",
     "PhD Cybersecurity", 2),
]

_LECTURER_QUALIFICATIONS = [
    ("L001", "PhD Computer Science", "University of Cambridge", 1938),
    ("L001", "BSc Mathematics", "King's College London", 1934),
    ("L002", "PhD Mathematics", "Yale University", 1934),
    ("L003", "PhD Electrical Engineering", "Graz University", 2005),
    ("L004", "PhD Finance", "London Business School", 2008),
    ("L005", "PhD Mathematics", "University of Gottingen", 1799),
    ("L006", "PhD Cybersecurity", "Imperial College London", 2012),
]

_LECTURER_RESEARCH_INTERESTS = [
    ("L001", 1), ("L002", 4), ("L003", 3),
    ("L004", 5), ("L005", 6), ("L006", 2), ("L001", 4),
]
# Expertise mirrors declared research interests for the demo.
_LECTURER_EXPERTISE = list(_LECTURER_RESEARCH_INTERESTS)

_PUBLICATIONS = [
    (1, "On Computable Numbers", "Proc. London Math. Society", "2023-05-10"),
    (2, "Neural Approaches to Data Science", "Journal of Data Science", "2024-02-18"),
    (3, "Compiler Design Revisited", "ACM Computing Surveys", "2022-11-03"),
    (4, "Modelling Financial Risk", "Journal of Finance", "2023-09-21"),
    (5, "Foundations of Cyber Defence", "IEEE Security & Privacy", "2024-06-01"),
]

_LECTURER_PUBLICATIONS = [
    ("L001", 1), ("L002", 2), ("L002", 3),
    ("L004", 4), ("L006", 5), ("L001", 2),
]

_COMMITTEES = [
    (1, "Admissions Committee"),
    (2, "Research Ethics Committee"),
    (3, "Curriculum Committee"),
]

_COMMITTEE_MEMBERSHIPS = [
    ("L001", 2), ("L001", 3), ("L004", 1), ("L002", 3), ("L006", 2),
]

_STUDENTS = [
    ("S001", "Alice Smith", "2003-04-12", "alice.smith@uni.edu", "+44 7700 900001", 1, 2, "Not Graduated", "L001"),
    ("S002", "Bob Jones", "2002-08-30", "bob.jones@uni.edu", "+44 7700 900002", 1, 3, "Not Graduated", "L001"),
    ("S003", "Carol White", "2004-01-05", "carol.white@uni.edu", "+44 7700 900003", 1, 1, "Not Graduated", "L002"),
    ("S004", "David Brown", "2000-06-22", "david.brown@uni.edu", "+44 7700 900004", 2, 1, "Not Graduated", "L002"),
    ("S005", "Eva Green", "2001-03-14", "eva.green@uni.edu", "+44 7700 900005", 3, 4, "Not Graduated", "L003"),
    ("S006", "Frank Black", "2003-09-09", "frank.black@uni.edu", "+44 7700 900006", 3, 2, "Not Graduated", "L003"),
    ("S007", "Grace Lee", "1999-12-01", "grace.lee@uni.edu", "+44 7700 900007", 4, 3, "Graduated", "L004"),
    ("S008", "Henry Ford", "2004-05-27", "henry.ford@uni.edu", "+44 7700 900008", 4, 1, "Not Graduated", "L004"),
    ("S009", "Ivy Chen", "2003-07-19", "ivy.chen@uni.edu", "+44 7700 900009", 6, 2, "Not Graduated", "L005"),
    ("S010", "Jack Ryan", "2002-02-08", "jack.ryan@uni.edu", "+44 7700 900010", 6, 3, "Not Graduated", "L005"),
    ("S011", "Kate Moss", "2000-10-16", "kate.moss@uni.edu", "+44 7700 900011", 2, 2, "Graduated", "L002"),
    ("S012", "Leo Martin", "2001-11-25", "leo.martin@uni.edu", "+44 7700 900012", 5, 1, "Not Graduated", "L004"),
]

_STUDENT_ORGANIZATIONS = [
    (1, "Coding Club"),
    (2, "Debate Society"),
    (3, "Chess Club"),
]

_STUDENT_ORG_MEMBERSHIPS = [
    ("S001", 1), ("S002", 1), ("S007", 2), ("S009", 3), ("S004", 1),
]

_DISCIPLINARY_RECORDS = [
    (1, "S003", "2024-10-02", "Late submission without approval", "Resolved"),
    (2, "S006", "2025-01-15", "Unauthorised absence from assessment", "Under Review"),
]

_COURSES = [
    ("CS101", "Introduction to Programming", 1, "Undergraduate", 15,
     "Fundamentals of programming using Python."),
    ("CS201", "Data Structures and Algorithms", 1, "Undergraduate", 20,
     "Core data structures, complexity and algorithm design."),
    ("CS501", "Machine Learning", 1, "Postgraduate", 20,
     "Supervised and unsupervised learning methods."),
    ("CS301", "Cybersecurity Fundamentals", 1, "Undergraduate", 20,
     "Principles of secure systems and threat modelling."),
    ("EE101", "Circuit Theory", 2, "Undergraduate", 15,
     "Analysis of linear electrical circuits."),
    ("BM101", "Principles of Management", 3, "Undergraduate", 15,
     "Introduction to management theory and practice."),
    ("MA101", "Calculus I", 4, "Undergraduate", 20,
     "Limits, differentiation and integration."),
]

_COURSE_PREREQUISITES = [
    ("CS201", "CS101"),
    ("CS301", "CS101"),
    ("CS501", "CS201"),
]

_COURSE_OFFERINGS = [
    (1, "CS101", "2024/25", "Autumn"),
    (2, "CS201", "2024/25", "Spring"),
    (3, "CS501", "2024/25", "Autumn"),
    (4, "CS301", "2024/25", "Spring"),
    (5, "EE101", "2024/25", "Autumn"),
    (6, "BM101", "2024/25", "Autumn"),
    (7, "MA101", "2024/25", "Autumn"),
]

_SCHEDULE_SLOTS = [
    (1, "Monday", "09:00", "11:00", "CS Lab 1"),
    (2, "Tuesday", "13:00", "15:00", "CS Lab 2"),
    (3, "Wednesday", "10:00", "12:00", "CS Seminar Room"),
    (4, "Thursday", "09:00", "11:00", "CS Lab 1"),
    (5, "Monday", "14:00", "16:00", "EE Lab A"),
    (6, "Friday", "11:00", "13:00", "BM Room 3"),
    (7, "Tuesday", "09:00", "11:00", "MA Room 1"),
]

_COURSE_MATERIALS = [
    (1, "Lecture Notes: Python Basics"),
    (1, "Lab Sheet 1"),
    (2, "Textbook: Introduction to Algorithms"),
    (2, "Problem Set 3"),
    (3, "Reading List: ML Foundations"),
    (4, "Slides: Threat Modelling"),
]

_TEACHING_ASSIGNMENTS = [
    ("L001", 1, "Primary"),
    ("L002", 2, "Primary"),
    ("L002", 3, "Primary"),
    ("L001", 3, "Assistant"),
    ("L006", 4, "Primary"),
    ("L003", 5, "Primary"),
    ("L004", 6, "Primary"),
    ("L005", 7, "Primary"),
]

_ENROLLMENTS = [
    (1, "S001", 1, "A", 85.0),
    (2, "S001", 2, "B", 78.0),
    (3, "S002", 2, "A", 90.0),
    (4, "S002", 4, "B", 75.0),
    (5, "S003", 1, "C", 65.0),
    (6, "S004", 3, "A", 88.0),
    (7, "S004", 2, "B", 80.0),
    (8, "S005", 5, "B", 72.0),
    (9, "S006", 5, "C", 68.0),
    (10, "S007", 6, "A", 91.0),
    (11, "S008", 6, "B", 74.0),
    (12, "S009", 7, "A", 95.0),
    (13, "S010", 7, "B", 79.0),
    (14, "S011", 3, "A", 89.0),
    (15, "S012", 6, "C", 66.0),
]

_NON_ACADEMIC_STAFF = [
    ("ST001", "Nancy Adams", "Department Administrator", 1, "Full-Time", "Permanent"),
    ("ST002", "Oscar Reid", "Laboratory Technician", 1, "Full-Time", "Fixed-Term"),
    ("ST003", "Paula Cruz", "Office Clerk", 2, "Part-Time", "Fixed-Term"),
    ("ST004", "Quentin Ford", "Finance Officer", 3, "Full-Time", "Permanent"),
    ("ST005", "Rita Bello", "Librarian", 4, "Part-Time", "Permanent"),
    ("ST006", "Sam Patel", "IT Support Officer", 1, "Full-Time", "Permanent"),
]

_PROGRAM_COURSE_REQUIREMENTS = [
    (1, "CS101", 15, "Semester 1", 1),
    (1, "CS201", 20, "Semester 2", 2),
    (1, "CS301", 20, "Semester 1", 3),
    (2, "CS501", 20, "Semester 1", 1),
    (3, "EE101", 15, "Semester 1", 1),
    (4, "BM101", 15, "Semester 1", 1),
    (6, "MA101", 20, "Semester 1", 1),
]

_RESEARCH_PROJECTS = [
    (1, "AI for Healthcare Diagnostics", "L001", 1, "Active", "2022-01-15", "2024-12-31"),
    (2, "Secure IoT Networks", "L006", 1, "Active", "2023-03-01", "2025-02-28"),
    (3, "Smart Grid Optimisation", "L003", 2, "Completed", "2021-06-01", "2023-05-31"),
    (4, "Financial Risk Modelling", "L004", 3, "Completed", "2021-09-01", "2022-08-31"),
]

_FUNDING_SOURCES = [
    (1, "National Science Foundation", "Government"),
    (2, "TechCorp Ltd", "Industry"),
    (3, "University Research Fund", "Internal"),
]

_PROJECT_FUNDING = [
    (1, 1, "$", 500000),
    (2, 2, "$", 300000),
    (3, 1, "$", 250000),
    (4, 3, "$", 120000),
]

_RESEARCH_PROJECT_TEAM = [
    (1, "Dr. Alan Turing", "Principal Investigator", "Computer Science"),
    (1, "Dr. Grace Hopper", "Co-Investigator", "Computer Science"),
    (1, "Bob Jones", "Research Assistant", "Computer Science"),
    (2, "Dr. Marie Secure", "Principal Investigator", "Computer Science"),
    (2, "Alice Smith", "Research Assistant", "Computer Science"),
    (3, "Dr. Nikola Volt", "Principal Investigator", "Electrical Engineering"),
    (4, "Prof. Ada Ledger", "Principal Investigator", "Business Management"),
]

_PROJECT_OUTCOMES = [
    (1, "Two peer-reviewed publications in medical AI."),
    (1, "Prototype diagnostic model with 92% accuracy."),
    (2, "Open-source secure IoT gateway released."),
    (3, "Grid loss reduced by 12% in field trials."),
    (4, "New risk model adopted by industry partner."),
]

_INSERTS = [
    ("DEPARTMENT", _DEPARTMENTS),
    ("RESEARCH_AREA", _RESEARCH_AREAS),
    ("DEPARTMENT_RESEARCH_AREA", _DEPARTMENT_RESEARCH_AREAS),
    ("PROGRAM", _PROGRAMS),
    ("LECTURER", _LECTURERS),
    ("LECTURER_QUALIFICATION", _LECTURER_QUALIFICATIONS),
    ("LECTURER_RESEARCH_INTEREST", _LECTURER_RESEARCH_INTERESTS),
    ("LECTURER_EXPERTISE", _LECTURER_EXPERTISE),
    ("PUBLICATION", _PUBLICATIONS),
    ("LECTURER_PUBLICATION", _LECTURER_PUBLICATIONS),
    ("COMMITTEE", _COMMITTEES),
    ("COMMITTEE_MEMBERSHIP", _COMMITTEE_MEMBERSHIPS),
    ("STUDENT", _STUDENTS),
    ("STUDENT_ORGANIZATION", _STUDENT_ORGANIZATIONS),
    ("STUDENT_ORG_MEMBERSHIP", _STUDENT_ORG_MEMBERSHIPS),
    ("DISCIPLINARY_RECORD", _DISCIPLINARY_RECORDS),
    ("COURSE", _COURSES),
    ("COURSE_PREREQUISITE", _COURSE_PREREQUISITES),
    ("COURSE_OFFERING", _COURSE_OFFERINGS),
    ("SCHEDULE_SLOT", _SCHEDULE_SLOTS),
    ("COURSE_MATERIAL", _COURSE_MATERIALS),
    ("TEACHING_ASSIGNMENT", _TEACHING_ASSIGNMENTS),
    ("ENROLLMENT", _ENROLLMENTS),
    ("NON_ACADEMIC_STAFF", _NON_ACADEMIC_STAFF),
    ("PROGRAM_COURSE_REQUIREMENT", _PROGRAM_COURSE_REQUIREMENTS),
    ("RESEARCH_PROJECT", _RESEARCH_PROJECTS),
    ("FUNDING_SOURCE", _FUNDING_SOURCES),
    ("PROJECT_FUNDING", _PROJECT_FUNDING),
    ("RESEARCH_PROJECT_TEAM", _RESEARCH_PROJECT_TEAM),
    ("PROJECT_OUTCOME", _PROJECT_OUTCOMES),
]


_COMPATIBILITY_ALIASES = {
    "NON_ACADEMIC_STAFF_UI": "NON_ACADEMIC_STAFF",
    "LECTURER_EXPERTISE_UI": "LECTURER_EXPERTISE",
    "PROJECT_FUNDING_UI": "PROJECT_FUNDING",
}


def build_in_memory() -> sqlite3.Connection:
    """Create and populate the in-memory demo database, returning the connection."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.executescript(_SCHEMA)
    for table, rows in _INSERTS:
        if not rows:
            continue
        placeholders = ", ".join(["?"] * len(rows[0]))
        cur.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)
    for alias, source in _COMPATIBILITY_ALIASES.items():
        cur.execute(f"CREATE TEMP VIEW {alias} AS SELECT * FROM {source}")
    conn.commit()
    return conn
