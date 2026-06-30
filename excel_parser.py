"""
excel_parser.py

Parses the SPCL dashboard workbook into a structure that the
Streamlit dashboard can easily use.
"""

from openpyxl.cell.cell import MergedCell

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------

IGNORE_HEADERS = [
    "TOTAL Smallholders",
    "TOTAL Serendipalm",
    "DAF Smallholders",
    "DAF Serendipalm",
    "TOTAL DAF",
    "TOTAL All Locations",
]

SMALLHOLDER_HEADERS = [
    "SPCL Smallholders",
    "Tanoobia Smallholders",
]


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def clean(value):
    if value is None:
        return ""

    return str(value).strip()


# ------------------------------------------------------------------
# Agriculture Structure
# ------------------------------------------------------------------

def agriculture_structure(sheet):

    structure = {
        "projects": {
            "Serendipalm": {
                "locations": {}
            },
            "SPCL Smallholders": {},
            "Tanoobia Smallholders": {}
        }
    }

    col = 2

    while col <= sheet.max_column:

        header = clean(sheet.cell(row=6, column=col).value)

        if header == "":
            col += 1
            continue

        if header in IGNORE_HEADERS:
            break

        years = [
            sheet.cell(row=7, column=col).value,
            sheet.cell(row=7, column=col + 1).value,
            sheet.cell(row=7, column=col + 2).value,
        ]

        # ----------------------------
        # Smallholder projects
        # ----------------------------

        if header in SMALLHOLDER_HEADERS:

            structure["projects"][header] = {
                "column": col,
                "years": years
            }

        # ----------------------------
        # Serendipalm locations
        # ----------------------------

        else:

            structure["projects"]["Serendipalm"]["locations"][header] = {
                "column": col,
                "years": years
            }

        col += 3

    return structure


# ------------------------------------------------------------------
# Metric Lookup
# ------------------------------------------------------------------

def get_metric(sheet, metric_name, column):

    for row in range(1, sheet.max_row + 1):

        value = clean(sheet.cell(row=row, column=1).value)

        if value == metric_name:

            return sheet.cell(row=row, column=column).value

    return None


# ------------------------------------------------------------------
# Year -> Column
# ------------------------------------------------------------------

def get_column(base_column, year):

    year_map = {
        2026: 0,
        2025: 1,
        2024: 2,
    }

    return base_column + year_map[year]
