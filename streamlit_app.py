import streamlit.components.v1 as components

from dashboard_utils import (
    load_workbook_from_dropbox,
    get_sheet,
)

from excel_parser import (
    agriculture_structure,
    get_column,
    get_metric,
    social_employee_data,
    social_fair_trade_data,
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
# FORMAT HELPERS
# ======================================================

def format_value(value):

    if value is None:
        return "—"

    if isinstance(value, (int, float)):

        if value == int(value):
            return f"{int(value):,}"

        return f"{value:,.2f}"

    return str(value)

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

    # -----------------------------
    # Load worksheet
    # -----------------------------
    ws = get_sheet(wb, "Agriculture")
    structure = agriculture_structure(ws)

    # -----------------------------
    # Project selector
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

        location = None

        years = structure["projects"][project]["years"]

        year = st.selectbox(
            "Year",
            years,
            key="agri_year"
        )

        base_column = structure["projects"][project]["column"]

    column = get_column(base_column, year)

    st.divider()

    # =================================================
    # LAND OVERVIEW
    # =================================================

    st.subheader("🌿 Land Overview")

    col1, col2, col3 = st.columns(3)

    total_land = get_metric(
        ws,
        "Total Land Surface (Ha)",
        column
    )

    certified = get_metric(
        ws,
        "Certified Organic (Ha)",
        column
    )

    conversion = get_metric(
        ws,
        "In Conversion (Ha)",
        column
    )

    with col1:
        st.metric(
            "Total Land Surface",
            format_value(total_land)
    )

    with col2:
        st.metric(
            "Certified Organic",
            format_value(certified)
    )

    with col3:
        st.metric(
            "In Conversion",
            format_value(conversion)
    )

    st.divider()

    # =================================================
    # PLANTATION
    # =================================================

    st.subheader("🌴 Plantation")

    col1, col2, col3 = st.columns(3)

    palm = get_metric(
        ws,
        "Palm Area (Ha)",
        column
    )

    conservation = get_metric(
        ws,
        "Conservation Area (Ha)",
        column
    )

    roc = get_metric(
        ws,
        "ROC (Ha)",
        column
    )

    with col1:
        st.metric(
            "Palm Area",
            format_value(palm)
        )

    with col2:
        st.metric(
            "Conservation Area",
            format_value(conservation)
        )

    with col3:
        st.metric(
            "ROC",
            format_value(roc)
        )

# ======================================================
# PRODUCTION
# ======================================================

with production_tab:

    st.header("🏭 Production")

    st.caption(
        "Live Production Dashboard maintained by the Quality Team."
    )

    components.iframe(
        "https://charts.serendipalm.com/",
        height=2400,
        scrolling=False
    )

# ======================================================
# SOCIAL
# ======================================================

with social_tab:

    st.header("👥 Social")

    st.caption(
        "Social impact data from the SPCL master workbook."
    )

    # --------------------------------------------------
    # Load Social worksheet
    # --------------------------------------------------

    social_ws = get_sheet(wb, "Social")

    # --------------------------------------------------
    # Year selector
    # --------------------------------------------------

    social_year = st.selectbox(
        "Year",
        [2026, 2025, 2024, 2023, 2022],
        key="social_year"
    )

    st.divider()

    # ==================================================
    # SERENDIPALM EMPLOYEES
    # ==================================================

    st.subheader("👷 Serendipalm Employees")

    employee_data = social_employee_data(
        social_ws
    )

    selected_employee_data = employee_data.get(
        social_year,
        []
    )

    # --------------------------------------------------
    # Employee totals
    # --------------------------------------------------

    total_male = 0
    total_female = 0

    for item in selected_employee_data:

        if item["Type"] == "Total":

            total_male = item["Male"]
            total_female = item["Female"]

    total_employees = total_male + total_female

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Employees",
            format_value(total_employees)
        )

    with col2:

        st.metric(
            "Male",
            format_value(total_male)
        )

    with col3:

        st.metric(
            "Female",
            format_value(total_female)
        )

    # --------------------------------------------------
    # Employee table
    # --------------------------------------------------

    employee_rows = []

    for item in selected_employee_data:

        if item["Type"] != "Total":

            total = (
                item["Male"] +
                item["Female"]
            )

            employee_rows.append({
                "Employee Type": item["Type"],
                "Male": item["Male"],
                "Female": item["Female"],
                "Total": total,
            })

    if employee_rows:

        employee_df = pd.DataFrame(
            employee_rows
        )

        st.dataframe(
            employee_df,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # Employee gender chart
    # --------------------------------------------------

    st.subheader(
        "Gender Distribution by Employee Type"
    )

    if employee_rows:

        chart_df = employee_df.set_index(
            "Employee Type"
        )[["Male", "Female"]]

        st.bar_chart(
            chart_df,
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # FAIR TRADE PREMIUM
    # ==================================================

    st.subheader(
        "🤝 Fair Trade Premium Spending"
    )

    fair_trade_data = social_fair_trade_data(
        social_ws
    )

    selected_fair_trade = fair_trade_data.get(
        social_year,
        []
    )

    # --------------------------------------------------
    # Total spending
    # --------------------------------------------------

    total_spending = 0

    for item in selected_fair_trade:

        if item["Category"] == "Total":

            total_spending = item["Amount"]

    st.metric(
        "Total Fair Trade Premium Spending",
        format_value(total_spending)
    )

    # --------------------------------------------------
    # Spending table
    # --------------------------------------------------

    spending_rows = []

    for item in selected_fair_trade:

        if item["Category"] != "Total":

            spending_rows.append({
                "Category": item["Category"],
                "Amount": item["Amount"],
            })

    if spending_rows:

        spending_df = pd.DataFrame(
            spending_rows
        )

        st.dataframe(
            spending_df,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------
    # Spending chart
    # --------------------------------------------------

    st.subheader(
        "Fair Trade Premium Spending by Category"
    )

    if spending_rows:

        spending_chart = spending_df.set_index(
            "Category"
        )[["Amount"]]

        st.bar_chart(
            spending_chart,
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # FAIR TRADE HISTORICAL TREND
    # ==================================================

    st.subheader(
        "📈 Fair Trade Premium Spending Over Time"
    )

    historical_rows = []

    for year in sorted(
        fair_trade_data.keys()
    ):

        year_total = 0

        for item in fair_trade_data[year]:

            if item["Category"] == "Total":

                year_total = item["Amount"]

        historical_rows.append({
            "Year": year,
            "Total Spending": year_total,
        })

    if historical_rows:

        historical_df = pd.DataFrame(
            historical_rows
        )

        historical_df = historical_df.set_index(
            "Year"
        )

        st.line_chart(
            historical_df[
                ["Total Spending"]
            ],
            use_container_width=True
        )

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
