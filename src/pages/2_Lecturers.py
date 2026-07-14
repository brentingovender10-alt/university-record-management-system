"""Lecturers list and lecturer profile view."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Lecturers")


def show_profile(lecturer_id: str) -> None:
    info = database.run_query(
        "SELECT l.*, d.DepartmentName FROM LECTURER l "
        "LEFT JOIN DEPARTMENT d ON d.DepartmentID = l.DepartmentID WHERE l.LecturerID = ?",
        (lecturer_id,),
    )
    if info.empty:
        st.error("Lecturer not found.")
        return
    r = info.iloc[0]

    st.caption("Lecturers  ›  Lecturer Profile")
    top = st.columns([4, 1])
    top[0].title("Lecturer Profile")
    if top[1].button("← Back", use_container_width=True):
        del st.session_state["lecturer_id"]
        st.rerun()

    left, right = st.columns(2)
    with left:
        theme.kv_block("Personal Information", [
            ("Lecturer ID:", r["LecturerID"]),
            ("Full Name:", r["FullName"]),
            ("Department:", r["DepartmentName"]),
            ("Email:", r["Email"]),
            ("Phone:", r["Phone"]),
            ("Office:", r["Office"]),
        ])
        st.markdown('<div class="urms-section"><h4>Academic Qualifications</h4>', unsafe_allow_html=True)
        quals = database.run_query(
            'SELECT DegreeName AS "Degree", Institution AS "Institution", AwardYear AS "Year" '
            "FROM LECTURER_QUALIFICATION WHERE LecturerID = ? ORDER BY AwardYear DESC",
            (lecturer_id,),
        )
        theme.render_table(quals)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="urms-section"><h4>Courses Taught</h4>', unsafe_allow_html=True)
        courses = database.run_query(
            """
            SELECT c.CourseCode AS "Course Code", c.CourseName AS "Course Name",
                   (SELECT COUNT(*) FROM ENROLLMENT e WHERE e.OfferingID = o.OfferingID) AS "Students Enrolled"
            FROM TEACHING_ASSIGNMENT t
            JOIN COURSE_OFFERING o ON o.OfferingID = t.OfferingID
            JOIN COURSE c ON c.CourseCode = o.CourseCode
            WHERE t.LecturerID = ?
            GROUP BY c.CourseCode, c.CourseName, o.OfferingID
            ORDER BY c.CourseCode
            """,
            (lecturer_id,),
        )
        theme.render_table(courses)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="urms-section"><h4>Advisees</h4>', unsafe_allow_html=True)
        advisees = database.run_query(
            'SELECT StudentID AS "Student ID", FullName AS "Student Name", YearOfStudy AS "Year" '
            "FROM STUDENT WHERE AdvisorLecturerID = ? ORDER BY StudentID",
            (lecturer_id,),
        )
        theme.render_table(advisees)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="urms-section"><h4>Research Interests &amp; Publications</h4>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    interests = database.run_query(
        "SELECT ra.AreaName FROM LECTURER_RESEARCH_INTEREST i "
        "JOIN RESEARCH_AREA ra ON ra.ResearchAreaID = i.ResearchAreaID WHERE i.LecturerID = ?",
        (lecturer_id,),
    )
    pubs = database.run_query(
        "SELECT p.Title, strftime('%Y', p.PublicationDate) AS Yr FROM LECTURER_PUBLICATION lp "
        "JOIN PUBLICATION p ON p.PublicationID = lp.PublicationID WHERE lp.LecturerID = ? "
        "ORDER BY p.PublicationDate DESC",
        (lecturer_id,),
    )
    c1.markdown("**Research Interests**\n\n" + ("\n".join(f"- {a}" for a in interests["AreaName"]) or "- None"))
    c2.markdown("**Recent Publications**\n\n" + (
        "\n".join(f"- {t}, {y}" for t, y in zip(pubs["Title"], pubs["Yr"])) or "- None"))
    st.markdown("</div>", unsafe_allow_html=True)

    committees = database.run_query(
        "SELECT c.CommitteeName FROM COMMITTEE_MEMBERSHIP m "
        "JOIN COMMITTEE c ON c.CommitteeID = m.CommitteeID WHERE m.LecturerID = ?",
        (lecturer_id,),
    )
    items = "".join(f"<li>{c}</li>" for c in committees["CommitteeName"]) or "<li>None</li>"
    st.markdown(
        f'<div class="urms-section"><h4>Committee Memberships</h4><ul>{items}</ul></div>',
        unsafe_allow_html=True,
    )


def show_list() -> None:
    st.title("Lecturers")

    search = st.text_input("Search", placeholder="Search by name or ID…", label_visibility="collapsed")
    f1, f2 = st.columns(2)
    depts = ["All"] + database.run_query("SELECT DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")[
        "DepartmentName"].tolist()
    dept = f1.selectbox("Department", depts)
    areas = ["All"] + database.run_query("SELECT AreaName FROM RESEARCH_AREA ORDER BY AreaName")["AreaName"].tolist()
    area = f2.selectbox("Area of Expertise", areas)

    df = database.run_query(
        """
        SELECT l.LecturerID, l.FullName, d.DepartmentName, l.QualificationSummary,
               l.CourseLoad, l.LecturerID AS Lid,
               (SELECT GROUP_CONCAT(ra.AreaName, ', ') FROM LECTURER_RESEARCH_INTEREST i
                    JOIN RESEARCH_AREA ra ON ra.ResearchAreaID = i.ResearchAreaID
                    WHERE i.LecturerID = l.LecturerID) AS Interests
        FROM LECTURER l
        LEFT JOIN DEPARTMENT d ON d.DepartmentID = l.DepartmentID
        ORDER BY l.LecturerID
        """
    )
    if search:
        s = search.lower()
        df = df[df["FullName"].str.lower().str.contains(s) | df["LecturerID"].str.lower().str.contains(s)]
    if dept != "All":
        df = df[df["DepartmentName"] == dept]
    if area != "All":
        expert_ids = database.run_query(
            "SELECT le.LecturerID FROM LECTURER_EXPERTISE_UI le "
            "JOIN RESEARCH_AREA ra ON ra.ResearchAreaID = le.ResearchAreaID WHERE ra.AreaName = ?",
            (area,),
        )["LecturerID"].tolist()
        df = df[df["LecturerID"].isin(expert_ids)]

    display = df.rename(columns={
        "LecturerID": "Lecturer ID", "FullName": "Full Name", "DepartmentName": "Department",
        "QualificationSummary": "Qualifications", "CourseLoad": "Course Load", "Interests": "Research Interests",
    })[["Lecturer ID", "Full Name", "Department", "Qualifications", "Course Load", "Research Interests"]]
    page = theme.paginate(display.reset_index(drop=True), key="lecturers")
    theme.render_table(page)

    st.write("")
    ids = df["LecturerID"].tolist()
    if ids:
        oc1, oc2 = st.columns([2, 1])
        chosen = oc1.selectbox("Lecturer", ids, label_visibility="collapsed")
        if oc2.button("View profile", use_container_width=True):
            st.session_state["lecturer_id"] = chosen
            st.rerun()


if "lecturer_id" in st.session_state:
    show_profile(st.session_state["lecturer_id"])
else:
    show_list()
