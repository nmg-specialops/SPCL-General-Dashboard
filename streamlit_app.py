import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from dashboard_utils import (
    load_workbook_from_dropbox,
    get_sheet,
    get_projects,
    get_locations,
    get_years,
    get_metric,
)

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

with agri_tab:

    st.header("🌱 Agriculture")

if workbook_loaded:

    ws = get_sheet(wb, "Agriculture")

    # -----------------------------
    # Read workbook structure
    # -----------------------------

    projects = get_projects(ws)

    if not projects:
        st.error("No projects found.")
        st.stop()

    project = st.selectbox(
        "Project",
        projects
    )

    locations = get_locations(
        ws,
        project
    )

    location = st.selectbox(
        "Location",
        locations
    )

    years = get_years(
        ws,
        project,
        location
    )

    year = st.selectbox(
        "Year",
        years
    )

    st.divider()

    st.subheader("Surface Land")

    total_surface = get_metric(
        ws,
        "Total Land Surface (Ha)",
        project,
        location,
        year
    )

    cert_surface = get_metric(
        ws,
        "Certified Organic (Ha)",
        project,
        location,
        year
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Total Land Surface",
            total_surface if total_surface else "—"
        )

    with c2:
        st.metric(
            "Certified Organic",
            cert_surface if cert_surface else "—"
        )

else:

    st.error(workbook_error)

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
