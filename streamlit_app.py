import streamlit as st

from pages.agriculture import agriculture_page
from pages.production import production_page
from pages.social import social_page
from pages.financial import financial_page
from pages.other import other_page
from pages.summary import summary_page

st.set_page_config(
    page_title="SPCL Dashboard",
    layout="wide"
)

st.title("SPCL Dashboard")

tab_summary, tab_agri, tab_prod, tab_social, tab_fin, tab_other = st.tabs([
    "📊 Summary",
    "🌱 Agriculture",
    "🏭 Production",
    "👥 Social",
    "💰 Financial",
    "📋 Other"
])

with tab_summary:
    summary_page()

with tab_agri:
    agriculture_page()

with tab_prod:
    production_page()

with tab_social:
    social_page()

with tab_fin:
    financial_page()

with tab_other:
    other_page()
