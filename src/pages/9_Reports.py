"""Reports - generate summary reports and export them."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Reports")
st.title("Reports")

REPORTS = {
    "Student Performance Report": {
        "icon": "🎓", "desc": "View grades and academic standing across all students",
        "sql": """
            SELECT s.StudentID AS "Student ID", s.FullName AS "Full Name", p.ProgramName AS "Program",
                   s.YearOfStudy AS "Year", ROUND(AVG(e.FinalGradePercent), 1) AS "Avg Grade (%)",
                   s.GraduationStatus AS "Status"
            FROM STUDENT s
            LEFT JOIN PROGRAM p ON p.ProgramID = s.ProgramID
            LEFT JOIN ENROLLMENT e ON e.StudentID = s.StudentID AND e.FinalGradePercent IS NOT NULL
            GROUP BY s.StudentID ORDER BY s.StudentID
        """,
    },
    "Lecturer Publication Report": {
        "icon": "📄", "desc": "List all publications by lecturers within a date range",
        "sql": """
            SELECT pub.Title AS "Title", l.FullName AS "Lecturer", pub.Venue AS "Venue",
                   pub.PublicationDate AS "Date"
            FROM PUBLICATION pub
            JOIN LECTURER_PUBLICATION lp ON lp.PublicationID = pub.PublicationID
            JOIN LECTURER l ON l.LecturerID = lp.LecturerID
            ORDER BY pub.PublicationDate DESC
        """,
    },
    "Department Statistics Report": {
        "icon": "📊", "desc": "Summary of staff, courses, and research per department",
        "sql": """
            SELECT d.DepartmentName AS "Department", d.Faculty AS "Faculty",
                   (SELECT COUNT(*) FROM NON_ACADEMIC_STAFF s WHERE s.DepartmentID=d.DepartmentID) AS "Staff",
                   (SELECT COUNT(*) FROM COURSE c WHERE c.DepartmentID=d.DepartmentID) AS "Courses",
                   (SELECT COUNT(*) FROM RESEARCH_PROJECT r WHERE r.DepartmentID=d.DepartmentID) AS "Projects"
            FROM DEPARTMENT d ORDER BY d.DepartmentName
        """,
    },
    "Research Projects Summary": {
        "icon": "🧪", "desc": "Overview of active and completed research projects",
        "sql": """
            SELECT rp.ProjectTitle AS "Project", l.FullName AS "PI", d.DepartmentName AS "Department",
                   rp.Status AS "Status", rp.StartDate AS "Start", rp.EndDate AS "End"
            FROM RESEARCH_PROJECT rp
            LEFT JOIN LECTURER l ON l.LecturerID = rp.PrincipalInvestigatorID
            LEFT JOIN DEPARTMENT d ON d.DepartmentID = rp.DepartmentID
            ORDER BY rp.Status, rp.ProjectTitle
        """,
    },
    "Enrollment Report": {
        "icon": "👥", "desc": "Breakdown of student enrollment by program and year",
        "sql": """
            SELECT p.ProgramName AS "Program", s.YearOfStudy AS "Year", COUNT(*) AS "Students"
            FROM STUDENT s LEFT JOIN PROGRAM p ON p.ProgramID = s.ProgramID
            GROUP BY p.ProgramName, s.YearOfStudy ORDER BY p.ProgramName, s.YearOfStudy
        """,
    },
    "Staff Employment Report": {
        "icon": "💼", "desc": "Summary of all staff by department and contract type",
        "sql": """
            SELECT st.StaffID AS "Staff ID", st.FullName AS "Full Name", d.DepartmentName AS "Department",
                   st.EmploymentType AS "Employment Type", st.ContractType AS "Contract Type"
            FROM NON_ACADEMIC_STAFF st LEFT JOIN DEPARTMENT d ON d.DepartmentID = st.DepartmentID
            ORDER BY d.DepartmentName, st.StaffID
        """,
    },
}

names = list(REPORTS)
cols = st.columns(3)
for i, name in enumerate(names):
    rep = REPORTS[name]
    with cols[i % 3]:
        st.markdown(
            f'<div class="urms-section" style="min-height:150px">'
            f'<div style="font-size:1.6rem">{rep["icon"]}</div>'
            f'<h4>{name}</h4><div style="color:#666;font-size:.9rem">{rep["desc"]}</div></div>',
            unsafe_allow_html=True,
        )
        if st.button("Generate", key=f"gen_{i}", use_container_width=True):
            st.session_state["report_name"] = name

st.divider()
st.subheader("Report Preview")
chosen = st.session_state.get("report_name")
if chosen:
    st.markdown(f"**{chosen}**")
    df = database.run_query(REPORTS[chosen]["sql"])
    theme.render_table(df)
    if not df.empty:
        st.download_button(
            "⬇  Export CSV", df.to_csv(index=False).encode("utf-8"),
            file_name=f"{chosen.lower().replace(' ', '_')}.csv", mime="text/csv",
        )
else:
    st.info("Select a report above and click **Generate** to preview it here.")
