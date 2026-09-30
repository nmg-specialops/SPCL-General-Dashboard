import requests
from io import BytesIO
from openpyxl import load_workbook
import streamlit as st


# =====================================================
# DROPBOX WORKBOOKS
# =====================================================

MASTER_DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/"
    "pm80k4kjyzqz8yez7sffu/"
    "SPCL_DataCollection-MasterSheet_forDASHBOARD.xlsx"
    "?rlkey=3zehft3tkllkl789hdptna4f3"
    "&st=phue6k1f"
    "&dl=1"
)

SOCIAL_DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/"
    "a2myfdhttdaxwlbvtm469/"
    "SPCL_SocialData_Input.xlsx"
    "?rlkey=v94zr4qcm4f93lg9coc6r9kbp"
    "&st=w3y8l7wf"
    "&dl=1"
)


def _load_workbook_from_url(url):
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    return load_workbook(
        BytesIO(response.content),
        data_only=True
    )


@st.cache_data(show_spinner=False)
def load_workbook_from_dropbox():
    """Load the main workbook used by the Agriculture tab."""
    return _load_workbook_from_url(MASTER_DROPBOX_URL)


@st.cache_data(show_spinner=False)
def load_social_workbook_from_dropbox():
    """Load the separate workbook used by the Social tab."""
    return _load_workbook_from_url(SOCIAL_DROPBOX_URL)


# =====================================================
# SHEET
# =====================================================

def get_sheet(workbook, sheet_name):
    return workbook[sheet_name]
