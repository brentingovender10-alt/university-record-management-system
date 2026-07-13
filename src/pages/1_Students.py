"""Students list and student profile view."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Students")


def show_profile(student_id: str) -> None:
    info = database.run_query(
        """
        SELECT s.*, p.ProgramName, l.FullName AS AdvisorName
        FROM STUDENT s
        LEFT JOIN PROGRAM p  ON p.ProgramID = s.ProgramID
        LEFT JOIN LECTURER l ON l.LecturerID = s.AdvisorLecturerID
        WHERE s.StudentID = ?
        """,
        (student_id,),
    )
    if info.empty:
        st.error("Student not found.")
        return
    r = info.iloc[0]

    st.caption("Students  ›  Student Profile")
    top = st.columns([4, 1])
    top[0].title("Student Profile")
    if top[1].button("← Back", use_container_width=True):
        del st.session_state["student_id"]
        st.rerun()

    left, right = st.columns(2)
    with left:
        theme.kv_block("Personal Information", [
            ("Student ID:", r["StudentID"]),
            ("Full Name:", r["FullName"]),
            ("Date of Birth:", r["DateOfBirth"]),
            ("Contact Email:", r["Email"]),
            ("Phone:", r["Phone"]),
        ])
        theme.kv_block("Academic Information", [
            ("Program:", r["ProgramName"]),
            ("Year of Study:", f'Year {r["YearOfStudy"]}'),
            ("Graduation Status:", r["GraduationStatus"]),
            ("Faculty Advisor:", r["AdvisorName"]),
        ])
    with right:
        st.markdown('<div class="urms-section"><h4>Enrolled Courses</h4>', unsafe_allow_html=True)
        courses = database.run_query(
            """
            SELECT c.CourseCode AS "Course Code", c.CourseName AS "Course Name",
                   l.FullName AS "Lecturer", e.GradeLetter AS "Grade"
            FROM ENROLLMENT e
            JOIN COURSE_OFFERING o ON o.OfferingID = e.OfferingID
            JOIN COURSE c ON c.CourseCode = o.CourseCode
            LEFT JOIN TEACHING_ASSIGNMENT t ON t.OfferingID = o.OfferingID AND t.TeachingRole='Primary'
            LEFT JOIN LECTURER l ON l.LecturerID = t.LecturerID
            WHERE e.StudentID = ?
            ORDER BY c.CourseCode
            """,
            (student_id,),
        )
        theme.render_table(courses)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="urms-section"><h4>Disciplinary Records</h4>', unsafe_allow_html=True)
        disc = database.run_query(
            'SELECT IncidentDate AS "Date", Description AS "Incident", Status FROM '
            "DISCIPLINARY_RECORD WHERE StudentID = ? ORDER BY IncidentDate DESC",
            (student_id,),
        )
        theme.render_table(disc)
        st.markdown("</div>", unsafe_allow_html=True)

        orgs = database.run_query(
            """
            SELECT o.OrgName FROM STUDENT_ORG_MEMBERSHIP m
            JOIN STUDENT_ORGANIZATION o ON o.OrgID = m.OrgID
            WHERE m.StudentID = ?
            """,
            (student_id,),
        )
        org_items = "".join(f"<li>{o}</li>" for o in orgs["OrgName"]) or "<li>None</li>"
        st.markdown(
            f'<div class="urms-section"><h4>Student Organizations</h4><ul>{org_items}</ul></div>',
            unsafe_allow_html=True,
        )


def show_list() -> None:
    st.title("Students")

    search = st.text_input("Search", placeholder="Search by name or ID…", label_visibility="collapsed")
    f1, f2, f3 = st.columns(3)
    depts = ["All"] + database.run_query("SELECT DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")[
        "DepartmentName"].tolist()
    dept = f1.selectbox("Department", depts)
    year = f2.selectbox("Year of Study", ["All", 1, 2, 3, 4])
    grad = f3.selectbox("Graduation Status", ["All", "Not Graduated", "Graduated"])

    df = database.run_query(
        """
        SELECT s.StudentID, s.FullName, p.ProgramName, s.YearOfStudy,
               l.FullName AS Advisor, s.GraduationStatus, d.DepartmentName
        FROM STUDENT s
        LEFT JOIN PROGRAM p    ON p.ProgramID = s.ProgramID
        LEFT JOIN LECTURER l   ON l.LecturerID = s.AdvisorLecturerID
        LEFT JOIN DEPARTMENT d ON d.DepartmentID = p.DepartmentID
        ORDER BY s.StudentID
        """
    )

    if search:
        s = search.lower()
        df = df[df["FullName"].str.lower().str.contains(s) | df["StudentID"].str.lower().str.contains(s)]
    if dept != "All":
        df = df[df["DepartmentName"] == dept]
    if year != "All":
        df = df[df["YearOfStudy"] == year]
    if grad != "All":
        df = df[df["GraduationStatus"] == grad]

    display = df.rename(columns={
        "StudentID": "Student ID", "FullName": "Full Name", "ProgramName": "Program",
        "YearOfStudy": "Year", "Advisor": "Faculty Advisor",
        "GraduationStatus": "Status",
    })[["Student ID", "Full Name", "Program", "Year", "Faculty Advisor", "Status"]]

    page = theme.paginate(display.reset_index(drop=True), key="students")
    theme.render_table(page, pill_columns=("Status",))

    st.write("")
    st.markdown("**Open a student profile**")
    ids = df["StudentID"].tolist()
    if ids:
        oc1, oc2 = st.columns([2, 1])
        chosen = oc1.selectbox("Student", ids, label_visibility="collapsed")
        if oc2.button("View profile", use_container_width=True):
            st.session_state["student_id"] = chosen
            st.rerun()


if "student_id" in st.session_state:
    show_profile(st.session_state["student_id"])
else:
    show_list()
