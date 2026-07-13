"""
University Record Management System - front end.

Entry point (Dashboard).  Run with:

    streamlit run src/Dashboard.py

The other screens live in ``src/pages`` and appear automatically in the
sidebar navigation.
"""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Dashboard")

st.title("Dashboard")


def _count(table: str) -> int:
    return int(database.scalar(f"SELECT COUNT(*) FROM {table}") or 0)


total_students = _count("STUDENT")
total_lecturers = _count("LECTURER")
total_courses = _count("COURSE")
total_departments = _count("DEPARTMENT")

row1 = st.columns(2)
row1[0].markdown(theme.stat_card("👥", "Total Students", f"{total_students:,}"), unsafe_allow_html=True)
row1[1].markdown(theme.stat_card("🧑‍🏫", "Total Lecturers", f"{total_lecturers:,}"), unsafe_allow_html=True)

st.write("")
row2 = st.columns(2)
row2[0].markdown(theme.stat_card("📖", "Total Courses", f"{total_courses:,}"), unsafe_allow_html=True)
row2[1].markdown(theme.stat_card("🏛️", "Total Departments", f"{total_departments:,}"), unsafe_allow_html=True)

st.write("")
st.subheader("Quick Actions")
qa = st.columns(3)
if qa[0].button("➕  Add Student", use_container_width=True):
    st.switch_page("pages/1_Students.py")
if qa[1].button("➕  Add Lecturer", use_container_width=True):
    st.switch_page("pages/2_Lecturers.py")
if qa[2].button("🔍  Run Query", use_container_width=True):
    st.switch_page("pages/8_Query_Builder.py")

st.write("")
st.caption(
    "This is the front-end interface. Data is served through a single database "
    "access layer (`urms/database.py`); it connects to `database/university.db` "
    "when that file is present, otherwise it uses bundled demo data."
)
