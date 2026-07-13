"""
Shared UI helpers: page setup, wireframe style (dark sidebar, black top bar, black-header data tables), and small render helpers.
"""

from __future__ import annotations

import html

import pandas as pd
import streamlit as st

from . import database

APP_TITLE = "University Record Management System"

_CSS = """
<style>
/* ---- Layout ---- */
.block-container { padding-top: 1.2rem; max-width: 1250px; }

/* ---- Dark sidebar (matches wireframes) ---- */
[data-testid="stSidebar"] { background-color: #17171a; }
[data-testid="stSidebar"] * { color: #f2f2f2 !important; }
[data-testid="stSidebar"] a { border-radius: 8px; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background-color: #4a4a4f; }

/* ---- Top banner ---- */
.urms-topbar {
    background: #17171a; color: #ffffff; padding: 16px 26px; border-radius: 10px;
    display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px;
}
.urms-topbar .brand { font-size: 1.35rem; font-weight: 700; letter-spacing: .2px; }
.urms-topbar .user { font-size: .95rem; opacity: .85; }

/* ---- Stat cards ---- */
.urms-card {
    border: 1px solid #e3e3e6; border-radius: 12px; padding: 18px 20px; background: #fff;
    display: flex; align-items: center; gap: 16px; min-height: 96px;
}
.urms-card .icon { font-size: 2rem; }
.urms-card .label { color: #555; font-size: .95rem; }
.urms-card .value { font-size: 2rem; font-weight: 800; line-height: 1.1; }

/* ---- Data tables (black header, striped rows) ---- */
.urms-table { width: 100%; border-collapse: collapse; font-size: .92rem; margin-top: .3rem; }
.urms-table th {
    background: #17171a; color: #fff; text-align: left; padding: 11px 14px; font-weight: 600;
}
.urms-table td { padding: 10px 14px; border-bottom: 1px solid #ececec; }
.urms-table tr:nth-child(even) td { background: #fafafa; }
.urms-table .pill {
    border: 1px solid #cfcfcf; border-radius: 14px; padding: 2px 12px; font-size: .82rem; background:#fff;
}

/* ---- Section headings inside detail cards ---- */
.urms-section { border:1px solid #e3e3e6; border-radius:12px; padding:16px 20px; background:#fff; margin-bottom:16px; }
.urms-section h4 { margin: 0 0 10px 0; }
.urms-kv { display:grid; grid-template-columns: 190px 1fr; row-gap:9px; font-size:.94rem; }
.urms-kv .k { color:#666; }
</style>
"""


def setup_page(active: str) -> None:
    """Standard page setup: config, CSS, top banner and sidebar footer."""
    st.set_page_config(page_title=f"{active} · URMS", page_icon="🎓", layout="wide")
    st.markdown(_CSS, unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="urms-topbar">
            <span class="brand">🎓 {APP_TITLE}</span>
            <span class="user">👤 Admin User ▾</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.caption(database.data_source_label())


def _cell(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return "—"
    return html.escape(str(value))


def render_table(df: pd.DataFrame, pill_columns: tuple[str, ...] = ()) -> None:
    """Render a DataFrame as a wireframe-styled HTML table."""
    if df is None or df.empty:
        st.info("No records to display.")
        return
    head = "".join(f"<th>{_cell(c)}</th>" for c in df.columns)
    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in df.columns:
            val = _cell(row[col])
            if col in pill_columns:
                val = f'<span class="pill">{val}</span>'
            cells.append(f"<td>{val}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    st.markdown(
        f'<table class="urms-table"><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>',
        unsafe_allow_html=True,
    )


def stat_card(icon: str, label: str, value) -> str:
    return (
        f'<div class="urms-card"><div class="icon">{icon}</div>'
        f'<div><div class="label">{html.escape(label)}</div>'
        f'<div class="value">{html.escape(str(value))}</div></div></div>'
    )


def kv_block(title: str, pairs: list[tuple[str, str]]) -> None:
    rows = "".join(
        f'<div class="k">{html.escape(k)}</div><div>{_cell(v)}</div>' for k, v in pairs
    )
    st.markdown(
        f'<div class="urms-section"><h4>{html.escape(title)}</h4><div class="urms-kv">{rows}</div></div>',
        unsafe_allow_html=True,
    )


def paginate(df: pd.DataFrame, key: str, page_size: int = 10) -> pd.DataFrame:
    """Simple pagination control; returns the current page slice."""
    total = len(df)
    if total <= page_size:
        st.caption(f"Showing {total} of {total} entries")
        return df
    pages = (total + page_size - 1) // page_size
    col1, col2 = st.columns([3, 1])
    with col2:
        page = st.number_input("Page", 1, pages, 1, key=f"page_{key}", label_visibility="collapsed")
    start = (page - 1) * page_size
    end = min(start + page_size, total)
    with col1:
        st.caption(f"Showing {start + 1}-{end} of {total} entries · page {page}/{pages}")
    return df.iloc[start:end]
