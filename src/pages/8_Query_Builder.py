"""
Query Builder - run any of the ten canned database queries.

The parameter widgets are generated dynamically from each query's spec in
``urms/queries.py``; the selected query's parametrised SQL is then executed in
Python via ``database.run_query`` and the results are shown and exportable.
"""

from __future__ import annotations

import streamlit as st

from urms import database, queries, theme

theme.setup_page("Query Builder")
st.title("Query Builder")

left, right = st.columns([1, 2])

with left:
    st.subheader("Select Query")
    labels = [f'{q["id"]}. {q["name"]}' for q in queries.QUERIES]
    idx = st.radio("Query", options=range(len(queries.QUERIES)),
                   format_func=lambda i: labels[i], label_visibility="collapsed")
    spec = queries.QUERIES[idx]

    st.subheader("Query Parameters")
    st.caption(spec["description"])

    values: dict = {}
    for p in spec["params"]:
        key = f"qb_{spec['id']}_{p['key']}"
        kind = p["kind"]
        if kind == "select":
            if "options_sql" in p:
                opts = database.run_query(p["options_sql"])
                pairs = list(zip(opts["value"], opts["label"]))
                if p.get("optional"):
                    pairs = [(None, "All Departments")] + pairs
                value_map = {label: val for val, label in pairs}
                choice = st.selectbox(p["label"], list(value_map))
                values[p["key"]] = value_map[choice]
            else:  # static options list
                choice = st.selectbox(p["label"], p["options"],
                                      index=p["options"].index(p.get("default", p["options"][0])))
                values[p["key"]] = choice
        elif kind == "number":
            values[p["key"]] = st.number_input(p["label"], value=int(p.get("default", 0)), step=1)
        elif kind == "date":
            values[p["key"]] = st.text_input(p["label"], value=p.get("default", ""))
        else:  # text
            values[p["key"]] = st.text_input(p["label"], value=p.get("default", ""),
                                             placeholder=p.get("placeholder", ""))

    run = st.button("▶  Execute Query", type="primary", use_container_width=True)
    if st.button("Clear", use_container_width=True):
        st.session_state.pop("qb_result", None)
        st.rerun()

with right:
    st.subheader("Query Results")
    if run:
        try:
            params = spec["bind"](values)
            st.session_state["qb_result"] = database.run_query(spec["sql"], params)
            st.session_state["qb_result_name"] = spec["name"]
        except Exception as exc:  # surface SQL / binding errors to the user
            st.error(f"Query failed: {exc}")
            st.session_state.pop("qb_result", None)

    result = st.session_state.get("qb_result")
    if result is not None:
        theme.render_table(result)
        st.caption(f"Showing {len(result)} result(s)")
        if not result.empty:
            csv = result.to_csv(index=False).encode("utf-8")
            fname = st.session_state.get("qb_result_name", "query").lower().replace(" ", "_")
            st.download_button("⬇  Export to CSV", csv, file_name=f"{fname}.csv", mime="text/csv")
    else:
        st.info("Select a query, set the parameters, and click **Execute Query**.")

with st.expander("Show SQL for the selected query"):
    st.code(spec["sql"].strip(), language="sql")
