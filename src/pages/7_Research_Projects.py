"""Research projects list and project details view."""

from __future__ import annotations

import streamlit as st

from urms import database, theme

theme.setup_page("Research Projects")


def show_details(project_id: int) -> None:
    info = database.run_query(
        "SELECT rp.*, l.FullName AS PIName, d.DepartmentName FROM RESEARCH_PROJECT rp "
        "LEFT JOIN LECTURER l ON l.LecturerID = rp.PrincipalInvestigatorID "
        "LEFT JOIN DEPARTMENT d ON d.DepartmentID = rp.DepartmentID WHERE rp.ProjectID = ?",
        (project_id,),
    )
    if info.empty:
        st.error("Project not found.")
        return
    r = info.iloc[0]

    st.caption("Research Projects  ›  Project Details")
    top = st.columns([4, 1])
    top[0].title("Project Details")
    if top[1].button("← Back", use_container_width=True):
        del st.session_state["project_id"]
        st.rerun()

    left, right = st.columns(2)
    with left:
        theme.kv_block("Project Information", [
            ("Project Title:", r["ProjectTitle"]),
            ("Principal Investigator:", r["PIName"]),
            ("Department:", r["DepartmentName"]),
            ("Status:", r["Status"]),
            ("Start Date:", r["StartDate"]),
            ("End Date:", r["EndDate"]),
        ])
        st.markdown('<div class="urms-section"><h4>Funding Sources</h4>', unsafe_allow_html=True)
        funding = database.run_query(
            """
            SELECT f.SourceName AS "Source",
                   (pf.Currency || format('%,d', pf.AmountAwarded)) AS "Amount",
                   f.SourceType AS "Type"
            FROM PROJECT_FUNDING_UI pf
            JOIN FUNDING_SOURCE f ON f.FundingSourceID = pf.FundingSourceID
            WHERE pf.ProjectID = ?
            """,
            (project_id,),
        )
        theme.render_table(funding)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="urms-section"><h4>Team Members</h4>', unsafe_allow_html=True)
        team = database.run_query(
            'SELECT MemberName AS "Name", ProjectRole AS "Role", DepartmentName AS "Department" '
            "FROM RESEARCH_PROJECT_TEAM WHERE ProjectID = ?",
            (project_id,),
        )
        theme.render_table(team)
        st.markdown("</div>", unsafe_allow_html=True)

        outcomes = database.run_query(
            "SELECT Description FROM PROJECT_OUTCOME WHERE ProjectID = ?", (project_id,)
        )["Description"].tolist()
        items = "".join(f"<li>{o}</li>" for o in outcomes) or "<li>None recorded</li>"
        st.markdown(
            f'<div class="urms-section"><h4>Outcomes</h4><ul>{items}</ul></div>',
            unsafe_allow_html=True,
        )


def show_list() -> None:
    st.title("Research Projects")
    search = st.text_input("Search", placeholder="Search by project title or PI…", label_visibility="collapsed")
    f1, f2, f3 = st.columns(3)
    depts = ["All"] + database.run_query("SELECT DepartmentName FROM DEPARTMENT ORDER BY DepartmentName")[
        "DepartmentName"].tolist()
    dept = f1.selectbox("Department", depts)
    status = f2.selectbox("Status", ["All", "Active", "Completed"])
    year = f3.selectbox("Year", ["All", 2021, 2022, 2023])

    df = database.run_query(
        """
        SELECT rp.ProjectID, rp.ProjectTitle, l.FullName AS PI, d.DepartmentName, rp.Status, rp.StartDate,
               (SELECT COUNT(*) FROM RESEARCH_PROJECT_TEAM t WHERE t.ProjectID = rp.ProjectID) AS TeamSize,
               (SELECT f.SourceName FROM PROJECT_FUNDING_UI pf
                    JOIN FUNDING_SOURCE f ON f.FundingSourceID = pf.FundingSourceID
                    WHERE pf.ProjectID = rp.ProjectID LIMIT 1) AS Funding
        FROM RESEARCH_PROJECT rp
        LEFT JOIN LECTURER l ON l.LecturerID = rp.PrincipalInvestigatorID
        LEFT JOIN DEPARTMENT d ON d.DepartmentID = rp.DepartmentID
        ORDER BY rp.ProjectTitle
        """
    )
    if search:
        s = search.lower()
        df = df[df["ProjectTitle"].str.lower().str.contains(s) | df["PI"].str.lower().str.contains(s)]
    if dept != "All":
        df = df[df["DepartmentName"] == dept]
    if status != "All":
        df = df[df["Status"] == status]
    if year != "All":
        df = df[df["StartDate"].str.startswith(str(year))]

    display = df.rename(columns={
        "ProjectTitle": "Project Title", "PI": "Principal Investigator", "DepartmentName": "Department",
        "Funding": "Funding Source", "TeamSize": "Team Size",
    })[["Project Title", "Principal Investigator", "Department", "Funding Source", "Status", "Team Size"]]
    page = theme.paginate(display.reset_index(drop=True), key="projects")
    theme.render_table(page, pill_columns=("Status",))

    st.write("")
    ids = df["ProjectID"].tolist()
    if ids:
        labels = {int(pid): title for pid, title in zip(df["ProjectID"], df["ProjectTitle"])}
        oc1, oc2 = st.columns([2, 1])
        chosen = oc1.selectbox("Project", list(labels), format_func=lambda x: labels[x],
                               label_visibility="collapsed")
        if oc2.button("View details", use_container_width=True):
            st.session_state["project_id"] = int(chosen)
            st.rerun()


if "project_id" in st.session_state:
    show_details(int(st.session_state["project_id"]))
else:
    show_list()
