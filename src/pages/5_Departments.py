"""Departments list with expandable detail rows."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from urms import database, theme

theme.setup_page("Departments")
st.title("Departments")

search = st.text_input("Search", placeholder="Search by department name…", label_visibility="collapsed")

df = database.run_query(
    """
    SELECT d.DepartmentID, d.DepartmentName, d.Faculty,
           (SELECT COUNT(*) FROM NON_ACADEMIC_STAFF_UI s WHERE s.DepartmentID = d.DepartmentID) AS Staff,
           (SELECT COUNT(*) FROM COURSE c WHERE c.DepartmentID = d.DepartmentID) AS Courses,
           (SELECT GROUP_CONCAT(ra.AreaName, ', ') FROM DEPARTMENT_RESEARCH_AREA dra
                JOIN RESEARCH_AREA ra ON ra.ResearchAreaID = dra.ResearchAreaID
                WHERE dra.DepartmentID = d.DepartmentID) AS ResearchAreas
    FROM DEPARTMENT d
    ORDER BY d.DepartmentName
    """
)
if search:
    df = df[df["DepartmentName"].str.lower().str.contains(search.lower())]

display = df.rename(columns={
    "DepartmentName": "Department Name", "Faculty": "Faculty", "Staff": "No. of Staff",
    "Courses": "No. of Courses", "ResearchAreas": "Research Areas",
})[["Department Name", "Faculty", "No. of Staff", "No. of Courses", "Research Areas"]]
theme.render_table(display.reset_index(drop=True))

st.write("")
for _, r in df.iterrows():
    with st.expander(f"🏛️  {r['DepartmentName']}"):
        c1, c2, c3 = st.columns(3)
        courses = database.run_query(
            "SELECT CourseName FROM COURSE WHERE DepartmentID = ? ORDER BY CourseName LIMIT 8",
            (int(r["DepartmentID"]),),
        )["CourseName"].tolist()
        staff = database.run_query(
            "SELECT FullName, JobTitle FROM NON_ACADEMIC_STAFF_UI WHERE DepartmentID = ? LIMIT 8",
            (int(r["DepartmentID"]),),
        )
        c1.markdown("**Courses Offered**\n\n" + ("\n".join(f"- {c}" for c in courses) or "- None"))
        c2.markdown("**Staff Members**\n\n" + (
            "\n".join(f"- {n} ({j})" for n, j in zip(staff["FullName"], staff["JobTitle"])) or "- None"))
        areas_raw = "" if pd.isna(r["ResearchAreas"]) else r["ResearchAreas"]
        c3.markdown("**Research Areas**\n\n" + (
            "\n".join(f"- {a}" for a in areas_raw.split(", ") if a) or "- None"))
