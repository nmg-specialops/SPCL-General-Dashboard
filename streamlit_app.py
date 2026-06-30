import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="SPCL General Dashboard",
    page_icon="🌍",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("SPCL General Dashboard")
st.caption("Live data loaded from the SPCL Master Workbook")

# --------------------------------------------------
# REFRESH BUTTON
# --------------------------------------------------

if st.button("🔄 Refresh Dashboard"):
    st.success("Dashboard refreshed.")

st.divider()

# --------------------------------------------------
# DASHBOARD TABS
# --------------------------------------------------

tab_summary, tab_agri, tab_prod, tab_social, tab_fin, tab_other = st.tabs(
    [
        "📊 Summary",
        "🌱 Agriculture",
        "🏭 Production",
        "👥 Social",
        "💰 Financial",
        "📋 Other"
    ]
)

# ==================================================
# SUMMARY
# ==================================================

with tab_summary:

    st.header("Executive Summary")

    st.info(
        "This page will be built after all dashboard sections are complete."
    )

# ==================================================
# AGRICULTURE
# ==================================================

with tab_agri:

    st.header("🌱 Agriculture")

    st.markdown("### Surface Land")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Metric 1", "—")

    with col2:
        st.metric("Metric 2", "—")

    with col3:
        st.metric("Metric 3", "—")

    st.divider()

    st.markdown("### Certified Land")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Metric 1", "—")

    with col2:
        st.metric("Metric 2", "—")

    with col3:
        st.metric("Metric 3", "—")

    st.divider()

    st.markdown("### DAF")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Metric 1", "—")

    with col2:
        st.metric("Metric 2", "—")

    with col3:
        st.metric("Metric 3", "—")

    st.divider()

    st.markdown("### Farmers")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Metric 1", "—")

    with col2:
        st.metric("Metric 2", "—")

    with col3:
        st.metric("Metric 3", "—")

    with col4:
        st.metric("Metric 4", "—")

# ==================================================
# PRODUCTION
# ==================================================

with tab_prod:

    st.header("🏭 Production")

    st.info("Production dashboard coming next.")

# ==================================================
# SOCIAL
# ==================================================

with tab_social:

    st.header("👥 Social")

    st.info("Social dashboard coming after Production.")

# ==================================================
# FINANCIAL
# ==================================================

with tab_fin:

    st.header("💰 Financial")

    st.info("Financial dashboard coming after Social.")

# ==================================================
# OTHER
# ==================================================

with tab_other:

    st.header("📋 Other")

    st.info("General worksheet information will appear here.")
