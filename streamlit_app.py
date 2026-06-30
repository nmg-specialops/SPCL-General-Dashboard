import streamlit as st
import requests
from io import BytesIO
from openpyxl import load_workbook

# -------------------------------------
# Dropbox Excel file
# -------------------------------------
DROPBOX_URL = "https://www.dropbox.com/scl/fi/pm80k4kjyzqz8yez7sffu/SPCL_DataCollection-MasterSheet_forDASHBOARD.xlsx?rlkey=3zehft3tkllkl789hdptna4f3&st=4cmf6srh&dl=1"

@st.cache_resource
def load_workbook_from_dropbox():

    response = requests.get(DROPBOX_URL)
    response.raise_for_status()

    workbook = load_workbook(
        BytesIO(response.content),
        data_only=True
    )

    return workbook

wb = load_workbook_from_dropbox()
ws = wb.active

import streamlit as st

st.set_page_config(
    page_title="SPCL Dashboard",
    layout="wide"
)

st.title("SPCL Dashboard")

# -------------------------------
# Navigation
# -------------------------------
tab_agri, tab_prod, tab_social, tab_fin, tab_other = st.tabs(
    [
        "🌱 Agriculture",
        "🏭 Production",
        "👥 Social",
        "💰 Financial",
        "📋 Other"
    ]
)

# =====================================================
# AGRICULTURE
# =====================================================
with tab_agri:
    st.header("Agriculture")
    st.info("Agriculture indicators will be added here.")

# =====================================================
# PRODUCTION
# =====================================================
with tab_prod:
    st.header("Production")
    st.info("Production indicators will be added here.")

# =====================================================
# SOCIAL
# =====================================================
with tab_social:

    st.header("Social")

    social_items = [
        "Education",
        "Water & Sanitation",
        "Infrastructure",
        "Other"
    ]

    for item in social_items:
        st.metric(
            label=item,
            value="0"
        )

# =====================================================
# FINANCIAL
# =====================================================
with tab_fin:
    st.header("Financial")
    st.info("Financial indicators will be added here.")

# =====================================================
# OTHER
# =====================================================
with tab_other:
    st.header("Other")
    st.info("Additional indicators will be added here.")
