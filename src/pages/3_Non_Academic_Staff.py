"""Non-academic staff list."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Non-Academic Staff")
st.title("Non-Academic Staff")

search = st.text_input("Search", placeholder="Search by name or staff ID…", label_visibility="collapsed")
f1, f2 = st.columns(2)
depts = ["All"] + database.run_query("SELECT DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")[
    "DepartmentName"].tolist()
dept = f1.selectbox("Department", depts)
emp = f2.selectbox("Employment Type", ["All", "Full-Time", "Part-Time"])

df = database.run_query(
    """
    SELECT st.StaffID, st.FullName, st.JobTitle, d.DepartmentName, st.EmploymentType, st.ContractType
    FROM NON_ACADEMIC_STAFF_UI st
    LEFT JOIN DEPARTMENT d ON d.DepartmentID = st.DepartmentID
    ORDER BY st.StaffID
    """
)
if search:
    s = search.lower()
    df = df[df["FullName"].str.lower().str.contains(s) | df["StaffID"].str.lower().str.contains(s)]
if dept != "All":
    df = df[df["DepartmentName"] == dept]
if emp != "All":
    df = df[df["EmploymentType"] == emp]

display = df.rename(columns={
    "StaffID": "Staff ID", "FullName": "Full Name", "JobTitle": "Job Title",
    "DepartmentName": "Department", "EmploymentType": "Employment Type", "ContractType": "Contract Type",
})
page = theme.paginate(display.reset_index(drop=True), key="staff")
theme.render_table(page)
