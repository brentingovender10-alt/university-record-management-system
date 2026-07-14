"""
Predefined queries for the Query Builder interface.

"""

from __future__ import annotations

QUERIES = [
    {
        "id": 1,
        "name": "Students by Department",
        "description": "List students in a chosen department (or all departments).",
        "params": [
            {
                "key": "dept",
                "kind": "select",
                "label": "Department",
                "options_sql": "SELECT DepartmentID AS value, DepartmentName AS label "
                               "FROM DEPARTMENT ORDER BY DepartmentName",
                "optional": True,
            },
        ],
        "sql": """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Full Name",
                   p.ProgramName AS "Program", s.YearOfStudy AS "Year"
            FROM STUDENT s
            JOIN PROGRAM p ON p.ProgramID = s.ProgramID
            WHERE (:dept IS NULL OR p.DepartmentID = :dept)
            ORDER BY s.StudentID
        """,
        "bind": lambda v: {"dept": v["dept"]},
    },
    {
        "id": 2,
        "name": "Students Enrolled in a Course",
        "description": "Show the students enrolled in a specific course, with their grades.",
        "params": [
            {
                "key": "course",
                "kind": "select",
                "label": "Course",
                "options_sql": "SELECT CourseCode AS value, (CourseCode || ' - ' || CourseName) AS label "
                               "FROM COURSE ORDER BY CourseCode",
            },
        ],
        "sql": """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Full Name",
                   e.GradeLetter AS "Grade", e.FinalGradePercent AS "Final %"
            FROM ENROLLMENT e
            JOIN COURSE_OFFERING o ON o.OfferingID = e.OfferingID
            JOIN STUDENT s ON s.StudentID = e.StudentID
            WHERE o.CourseCode = ?
            ORDER BY s.StudentID
        """,
        "bind": lambda v: (v["course"],),
    },
    {
        "id": 3,
        "name": "Courses Taught by a Lecturer",
        "description": "List the courses a chosen lecturer is assigned to teach.",
        "params": [
            {
                "key": "lecturer",
                "kind": "select",
                "label": "Lecturer",
                "options_sql": "SELECT LecturerID AS value, FullName AS label "
                               "FROM LECTURER ORDER BY FullName",
            },
        ],
        "sql": """
            SELECT DISTINCT c.CourseCode AS "Course Code", c.CourseName AS "Course Name",
                   t.TeachingRole AS "Role"
            FROM TEACHING_ASSIGNMENT t
            JOIN COURSE_OFFERING o ON o.OfferingID = t.OfferingID
            JOIN COURSE c ON c.CourseCode = o.CourseCode
            WHERE t.LecturerID = ?
            ORDER BY c.CourseCode
        """,
        "bind": lambda v: (v["lecturer"],),
    },
    {
        "id": 4,
        "name": "Lecturers in a Research Area",
        "description": "Find lecturers with expertise in a chosen research area.",
        "params": [
            {
                "key": "area",
                "kind": "select",
                "label": "Research Area",
                "options_sql": "SELECT ResearchAreaID AS value, AreaName AS label "
                               "FROM RESEARCH_AREA ORDER BY AreaName",
            },
        ],
        "sql": """
            SELECT l.LecturerID AS "Lecturer ID", l.FullName AS "Full Name",
                   d.DepartmentName AS "Department"
            FROM LECTURER_EXPERTISE_UI le
            JOIN LECTURER l ON l.LecturerID = le.LecturerID
            LEFT JOIN DEPARTMENT d ON d.DepartmentID = l.DepartmentID
            WHERE le.ResearchAreaID = ?
            ORDER BY l.FullName
        """,
        "bind": lambda v: (v["area"],),
    },
    {
        "id": 5,
        "name": "Students by Year of Study",
        "description": "List all students in a given year of study.",
        "params": [
            {
                "key": "year",
                "kind": "select",
                "label": "Year of Study",
                "options": [1, 2, 3, 4],
                "default": 1,
            },
        ],
        "sql": """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Full Name",
                   p.ProgramName AS "Program"
            FROM STUDENT s
            LEFT JOIN PROGRAM p ON p.ProgramID = s.ProgramID
            WHERE s.YearOfStudy = ?
            ORDER BY s.StudentID
        """,
        "bind": lambda v: (v["year"],),
    },
    {
        "id": 6,
        "name": "Research Projects by Status",
        "description": "List research projects that are active or completed.",
        "params": [
            {
                "key": "status",
                "kind": "select",
                "label": "Status",
                "options": ["Active", "Completed"],
                "default": "Active",
            },
        ],
        "sql": """
            SELECT rp.ProjectTitle AS "Project", l.FullName AS "Principal Investigator",
                   d.DepartmentName AS "Department", rp.StartDate AS "Start", rp.EndDate AS "End"
            FROM RESEARCH_PROJECT rp
            LEFT JOIN LECTURER l ON l.LecturerID = rp.PrincipalInvestigatorID
            LEFT JOIN DEPARTMENT d ON d.DepartmentID = rp.DepartmentID
            WHERE rp.Status = ?
            ORDER BY rp.ProjectTitle
        """,
        "bind": lambda v: (v["status"],),
    },
    {
        "id": 7,
        "name": "High-Performing Students",
        "description": "Students whose average final grade is at or above a threshold.",
        "params": [
            {
                "key": "threshold",
                "kind": "number",
                "label": "Minimum average grade (%)",
                "default": 75,
            },
        ],
        "sql": """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Full Name",
                   ROUND(AVG(e.FinalGradePercent), 1) AS "Average %"
            FROM STUDENT s
            JOIN ENROLLMENT e ON e.StudentID = s.StudentID
            WHERE e.FinalGradePercent IS NOT NULL
            GROUP BY s.StudentID, s.FullName
            HAVING AVG(e.FinalGradePercent) >= ?
            ORDER BY AVG(e.FinalGradePercent) DESC
        """,
        "bind": lambda v: (v["threshold"],),
    },
    {
        "id": 8,
        "name": "Course Enrolment Counts",
        "description": "Number of students enrolled in each course (no parameters).",
        "params": [],
        "sql": """
            SELECT c.CourseCode AS "Course Code", c.CourseName AS "Course Name",
                   COUNT(e.StudentID) AS "Enrolled"
            FROM COURSE c
            LEFT JOIN COURSE_OFFERING o ON o.CourseCode = c.CourseCode
            LEFT JOIN ENROLLMENT e ON e.OfferingID = o.OfferingID
            GROUP BY c.CourseCode, c.CourseName
            ORDER BY COUNT(e.StudentID) DESC, c.CourseCode
        """,
        "bind": lambda v: (),
    },
    {
        "id": 9,
        "name": "Publications Since a Date",
        "description": "Lecturer publications on or after a given date.",
        "params": [
            {
                "key": "since",
                "kind": "date",
                "label": "Published on or after (YYYY-MM-DD)",
                "default": "2023-01-01",
            },
        ],
        "sql": """
            SELECT pub.Title AS "Title", l.FullName AS "Lecturer",
                   pub.Venue AS "Venue", pub.PublicationDate AS "Date"
            FROM PUBLICATION pub
            JOIN LECTURER_PUBLICATION lp ON lp.PublicationID = pub.PublicationID
            JOIN LECTURER l ON l.LecturerID = lp.LecturerID
            WHERE pub.PublicationDate >= ?
            ORDER BY pub.PublicationDate DESC
        """,
        "bind": lambda v: (v["since"],),
    },
    {
        "id": 10,
        "name": "Staff by Employment Type",
        "description": "List non-academic staff of a chosen employment type.",
        "params": [
            {
                "key": "etype",
                "kind": "select",
                "label": "Employment Type",
                "options": ["Full-Time", "Part-Time"],
                "default": "Full-Time",
            },
        ],
        "sql": """
            SELECT st.StaffID AS "Staff ID", st.FullName AS "Full Name",
                   st.JobTitle AS "Job Title", d.DepartmentName AS "Department",
                   st.ContractType AS "Contract Type"
            FROM NON_ACADEMIC_STAFF_UI st
            LEFT JOIN DEPARTMENT d ON d.DepartmentID = st.DepartmentID
            WHERE st.EmploymentType = ?
            ORDER BY st.StaffID
        """,
        "bind": lambda v: (v["etype"],),
    },
]
