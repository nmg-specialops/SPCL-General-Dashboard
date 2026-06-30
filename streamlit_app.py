from dashboard_utils import (
    load_workbook_from_dropbox,
    get_sheet,
)

from excel_parser import (
    agriculture_structure,
    get_column,
    get_metric,
)

import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# ======================================================
# CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="SPCL General Dashboard",
    page_icon="🌍",
    layout="wide"
)

DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/"
    "pm80k4kjyzqz8yez7sffu/"
    "SPCL_DataCollection-MasterSheet_forDASHBOARD.xlsx"
    "?rlkey=3zehft3tkllkl789hdptna4f3"
    "&st=phue6k1f"
    "&dl=1"
)

# ======================================================
# LOAD WORKBOOK
# ======================================================

# ======================================================
# LOAD DATA
# ======================================================

try:

    wb = load_workbook_from_dropbox()

    workbook_loaded = True

except Exception as e:

    workbook_loaded = False

    workbook_error = str(e)

# ======================================================
# TITLE
# ======================================================

st.title("🌍 SPCL General Dashboard")

st.caption("Live data from Dropbox Excel Workbook")

col1, col2 = st.columns([1,1])

with col1:

    if st.button("🔄 Refresh Dashboard"):

        st.cache_data.clear()

        st.rerun()

with col2:

    if workbook_loaded:

        st.success("Workbook Connected")

    else:

        st.error("Workbook Not Connected")

st.divider()

# ======================================================
# TABS
# ======================================================

summary_tab, agri_tab, production_tab, social_tab, financial_tab, other_tab = st.tabs(
    [
        "📊 Summary",
        "🌱 Agriculture",
        "🏭 Production",
        "👥 Social",
        "💰 Financial",
        "📋 Other"
    ]
)

# ======================================================
# SUMMARY
# ======================================================

with summary_tab:

    st.header("Executive Summary")

    st.info("Summary dashboard will be added after all sections are complete.")

# ======================================================
# AGRICULTURE
# ======================================================
# ======================================================
# AGRICULTURE
# ======================================================

with agri_tab:

    st.header("🌱 Agriculture")

    # Load Agriculture worksheet
    ws = get_sheet(wb, "Agriculture")

    structure = agriculture_structure(ws)

    # -----------------------------
    # Project
    # -----------------------------

    projects = list(structure["projects"].keys())

    project = st.selectbox(
        "Project",
        projects,
        key="agri_project"
    )

    # -----------------------------
    # Serendipalm
    # -----------------------------

    if project == "Serendipalm":

        locations = list(
            structure["projects"]["Serendipalm"]["locations"].keys()
        )

        location = st.selectbox(
            "Location",
            locations,
            key="agri_location"
        )

        years = structure["projects"]["Serendipalm"]["locations"][location]["years"]

        year = st.selectbox(
            "Year",
            years,
            key="agri_year"
        )

        base_column = structure["projects"]["Serendipalm"]["locations"][location]["column"]

    # -----------------------------
    # Smallholders / Tanoobia
    # -----------------------------

    else:

        years = structure["projects"][project]["years"]

        year = st.selectbox(
            "Year",
            years,
            key="agri_year"
        )

        base_column = structure["projects"][project]["column"]

    column = get_column(base_column, year)

    st.divider()

    st.subheader("Surface Land")

    value = get_metric(
        ws,
        "Total Land Surface (Ha)",
        column
    )

    st.metric(
        "Total Land Surface",
        value if value is not None else "—"
    )

# ======================================================
# PRODUCTION
# ======================================================

with production_tab:

    st.header("🏭 Production")

    st.info("Coming soon.")

# ======================================================
# SOCIAL
# ======================================================

with social_tab:

    st.header("👥 Social")

    st.info("Coming soon.")

# ======================================================
# FINANCIAL
# ======================================================

with financial_tab:

    st.header("💰 Financial")

    st.info("Coming soon.")

# ======================================================
# OTHER
# ======================================================

with other_tab:

    st.header("📋 Other")

    st.info("General worksheet will appear here.")
