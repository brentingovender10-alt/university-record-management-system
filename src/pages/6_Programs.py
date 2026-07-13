"""Programs list with a detail side panel."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Programs")
st.title("Programs")

search = st.text_input("Search", placeholder="Search by program name…", label_visibility="collapsed")
f1, f2 = st.columns(2)
degree = f1.selectbox("Degree Type", ["All", "Bachelor of Science", "Bachelor of Engineering",
                                      "Master of Science", "Master of Business Administration",
                                      "Bachelor of Business Administration"])
duration = f2.selectbox("Duration", ["All", 2, 3, 4])

df = database.run_query(
    """
    SELECT pr.ProgramID, pr.ProgramName, pr.DegreeAwarded, pr.DurationYears, d.DepartmentName,
           (SELECT COUNT(*) FROM STUDENT s WHERE s.ProgramID = pr.ProgramID) AS Enrolled
    FROM PROGRAM pr
    LEFT JOIN DEPARTMENT d ON d.DepartmentID = pr.DepartmentID
    ORDER BY pr.ProgramName
    """
)
if search:
    df = df[df["ProgramName"].str.lower().str.contains(search.lower())]
if degree != "All":
    df = df[df["DegreeAwarded"] == degree]
if duration != "All":
    df = df[df["DurationYears"] == duration]

left, right = st.columns([3, 2])

with left:
    display = df.rename(columns={
        "ProgramName": "Program Name", "DegreeAwarded": "Degree Awarded",
        "DurationYears": "Duration", "DepartmentName": "Department", "Enrolled": "Enrolled Students",
    }).copy()
    display["Duration"] = display["Duration"].astype(str) + " years"
    theme.render_table(
        display[["Program Name", "Degree Awarded", "Duration", "Department", "Enrolled Students"]].reset_index(drop=True))

    names = df["ProgramName"].tolist()
    chosen = st.selectbox("View program details", names) if names else None

with right:
    if chosen is not None:
        pr = df[df["ProgramName"] == chosen].iloc[0]
        st.markdown(f"### {pr['ProgramName']}")
        st.caption(f"{pr['DegreeAwarded']} · {pr['DurationYears']} years · {pr['DepartmentName']}")

        st.markdown("**Course Requirements**")
        reqs = database.run_query(
            """
            SELECT r.CourseCode AS "Course Code", c.CourseName AS "Course Name",
                   r.Credits AS "Credits", r.Semester AS "Semester"
            FROM PROGRAM_COURSE_REQUIREMENT r
            JOIN COURSE c ON c.CourseCode = r.CourseCode
            WHERE r.ProgramID = ?
            ORDER BY r.RecommendedYear, r.Semester
            """,
            (int(pr["ProgramID"]),),
        )
        theme.render_table(reqs)

        st.markdown("**Enrollment Details**")
        st.metric("Total Enrolled (Active Students)", int(pr["Enrolled"]))
