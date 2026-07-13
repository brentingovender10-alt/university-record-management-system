"""Courses list and course details view."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Courses")


def show_details(course_code: str) -> None:
    info = database.run_query(
        "SELECT c.*, d.DepartmentName FROM COURSE c "
        "LEFT JOIN DEPARTMENT d ON d.DepartmentID = c.DepartmentID WHERE c.CourseCode = ?",
        (course_code,),
    )
    if info.empty:
        st.error("Course not found.")
        return
    r = info.iloc[0]
    prereqs = database.run_query(
        "SELECT PrereqCourseCode FROM COURSE_PREREQUISITE WHERE CourseCode = ?", (course_code,)
    )["PrereqCourseCode"].tolist()

    st.caption("Courses  ›  Course Details")
    top = st.columns([4, 1])
    top[0].title("Course Details")
    if top[1].button("← Back", use_container_width=True):
        del st.session_state["course_code"]
        st.rerun()

    left, right = st.columns(2)
    with left:
        theme.kv_block("Course Information", [
            ("Course Code:", r["CourseCode"]),
            ("Course Name:", r["CourseName"]),
            ("Department:", r["DepartmentName"]),
            ("Level:", r["Level"]),
            ("Credits:", r["Credits"]),
            ("Description:", r["Description"]),
            ("Prerequisites:", ", ".join(prereqs) if prereqs else "None"),
        ])
        st.markdown('<div class="urms-section"><h4>Schedule</h4>', unsafe_allow_html=True)
        sched = database.run_query(
            """
            SELECT s.DayOfWeek AS "Day", (s.StartTime || ' - ' || s.EndTime) AS "Time", s.Room AS "Venue"
            FROM SCHEDULE_SLOT s
            JOIN COURSE_OFFERING o ON o.OfferingID = s.OfferingID
            WHERE o.CourseCode = ?
            """,
            (course_code,),
        )
        theme.render_table(sched)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="urms-section"><h4>Assigned Lecturers</h4>', unsafe_allow_html=True)
        lecs = database.run_query(
            """
            SELECT DISTINCT l.LecturerID AS "Lecturer ID", l.FullName AS "Name", t.TeachingRole AS "Role"
            FROM TEACHING_ASSIGNMENT t
            JOIN COURSE_OFFERING o ON o.OfferingID = t.OfferingID
            JOIN LECTURER l ON l.LecturerID = t.LecturerID
            WHERE o.CourseCode = ?
            """,
            (course_code,),
        )
        theme.render_table(lecs)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="urms-section"><h4>Enrolled Students</h4>', unsafe_allow_html=True)
        studs = database.run_query(
            """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Name", s.YearOfStudy AS "Year", e.GradeLetter AS "Grade"
            FROM ENROLLMENT e
            JOIN COURSE_OFFERING o ON o.OfferingID = e.OfferingID
            JOIN STUDENT s ON s.StudentID = e.StudentID
            WHERE o.CourseCode = ?
            ORDER BY s.StudentID
            """,
            (course_code,),
        )
        theme.render_table(studs)
        st.markdown("</div>", unsafe_allow_html=True)

        mats = database.run_query(
            "SELECT DISTINCT m.Title FROM COURSE_MATERIAL m "
            "JOIN COURSE_OFFERING o ON o.OfferingID = m.OfferingID WHERE o.CourseCode = ?",
            (course_code,),
        )
        items = "".join(f"<li>{t}</li>" for t in mats["Title"]) or "<li>None</li>"
        st.markdown(
            f'<div class="urms-section"><h4>Course Materials</h4><ul>{items}</ul></div>',
            unsafe_allow_html=True,
        )


def show_list() -> None:
    st.title("Courses")
    search = st.text_input("Search", placeholder="Search by course code or name…", label_visibility="collapsed")
    f1, f2, f3 = st.columns(3)
    depts = ["All"] + database.run_query("SELECT DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")[
        "DepartmentName"].tolist()
    dept = f1.selectbox("Department", depts)
    level = f2.selectbox("Level", ["All", "Undergraduate", "Postgraduate"])
    credits = f3.selectbox("Credits", ["All", 15, 20])

    df = database.run_query(
        """
        SELECT c.CourseCode, c.CourseName, d.DepartmentName, c.Level, c.Credits,
               (SELECT l.FullName FROM TEACHING_ASSIGNMENT t
                    JOIN COURSE_OFFERING o ON o.OfferingID = t.OfferingID
                    JOIN LECTURER l ON l.LecturerID = t.LecturerID
                    WHERE o.CourseCode = c.CourseCode AND t.TeachingRole='Primary' LIMIT 1) AS Lecturer,
               (SELECT COUNT(*) FROM ENROLLMENT e
                    JOIN COURSE_OFFERING o ON o.OfferingID = e.OfferingID
                    WHERE o.CourseCode = c.CourseCode) AS Enrolled
        FROM COURSE c
        LEFT JOIN DEPARTMENT d ON d.DepartmentID = c.DepartmentID
        ORDER BY c.CourseCode
        """
    )
    if search:
        s = search.lower()
        df = df[df["CourseName"].str.lower().str.contains(s) | df["CourseCode"].str.lower().str.contains(s)]
    if dept != "All":
        df = df[df["DepartmentName"] == dept]
    if level != "All":
        df = df[df["Level"] == level]
    if credits != "All":
        df = df[df["Credits"] == credits]

    display = df.rename(columns={
        "CourseCode": "Course Code", "CourseName": "Course Name", "DepartmentName": "Department",
    })[["Course Code", "Course Name", "Department", "Level", "Credits", "Lecturer", "Enrolled"]]
    page = theme.paginate(display.reset_index(drop=True), key="courses")
    theme.render_table(page)

    st.write("")
    codes = df["CourseCode"].tolist()
    if codes:
        oc1, oc2 = st.columns([2, 1])
        chosen = oc1.selectbox("Course", codes, label_visibility="collapsed")
        if oc2.button("View details", use_container_width=True):
            st.session_state["course_code"] = chosen
            st.rerun()


if "course_code" in st.session_state:
    show_details(st.session_state["course_code"])
else:
    show_list()
