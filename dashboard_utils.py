import requests
from io import BytesIO
from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell
import streamlit as st

# =====================================================
# DROPBOX
# =====================================================

DROPBOX_URL = (
    "https://www.dropbox.com/scl/fi/"
    "pm80k4kjyzqz8yez7sffu/"
    "SPCL_DataCollection-MasterSheet_forDASHBOARD.xlsx"
    "?rlkey=3zehft3tkllkl789hdptna4f3"
    "&st=phue6k1f"
    "&dl=1"
)

# =====================================================
# LOAD WORKBOOK
# =====================================================

@st.cache_data(show_spinner=False)
def load_workbook_from_dropbox():

    response = requests.get(DROPBOX_URL)

    response.raise_for_status()

    workbook = load_workbook(
        BytesIO(response.content),
        data_only=True
    )

    return workbook


# =====================================================
# SHEET
# =====================================================

def get_sheet(workbook, sheet_name):
    return workbook[sheet_name]
