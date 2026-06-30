import requests
from io import BytesIO
from openpyxl import load_workbook
import streamlit as st

# =====================================================
# DROPBOX LINK
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
    """
    Downloads the Excel workbook from Dropbox and
    returns an openpyxl workbook object.
    """

    response = requests.get(DROPBOX_URL)
    response.raise_for_status()

    workbook = load_workbook(
        filename=BytesIO(response.content),
        data_only=True
    )

    return workbook

# =====================================================
# GET WORKSHEET
# =====================================================

def get_sheet(workbook, sheet_name):
    """Return a worksheet by name."""

    if sheet_name in workbook.sheetnames:
        return workbook[sheet_name]

    return None

# =====================================================
# FIND A ROW BY LABEL
# =====================================================

def find_row(sheet, label):
    """
    Searches Column A for a label and
    returns the row number.
    """

    for row in range(1, sheet.max_row + 1):

        value = sheet.cell(row=row, column=1).value

        if value == label:
            return row

    return None

# =====================================================
# GET CELL VALUE
# =====================================================

def get_value(sheet, row, column):
    """
    Returns a worksheet value.
    Blank cells become None.
    """

    value = sheet.cell(row=row, column=column).value

    if value == "":
        return None

    return value
