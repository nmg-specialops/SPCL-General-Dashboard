"""
excel_parser.py

Parses the Agriculture worksheet into a structure that the
Streamlit dashboard can use.
"""

# ============================================================
# HELPERS
# ============================================================

def clean(value):
    if value is None:
        return ""
    return str(value).strip()


# ============================================================
# AGRICULTURE STRUCTURE
# ============================================================

def agriculture_structure(sheet):

    structure = {
        "projects": {
            "All Projects": {},
            "Serendipalm": {
                "locations": {}
            },
            "SPCL Smallholders": {},
            "Tanoobia Smallholders": {},
        }
    }

    col = 2

    while col <= sheet.max_column:

        header = clean(sheet.cell(row=6, column=col).value)

        if header == "":
            col += 1
            continue

        years = [
            sheet.cell(row=7, column=col).value,
            sheet.cell(row=7, column=col + 1).value,
            sheet.cell(row=7, column=col + 2).value,
        ]

        # --------------------------------------------
        # Workbook totals
        # --------------------------------------------

        if header == "TOTAL All Locations":

            structure["projects"]["All Projects"] = {
                "column": col,
                "years": years,
            }

            break

        elif header == "TOTAL Serendipalm":

            structure["projects"]["Serendipalm"]["column"] = col
            structure["projects"]["Serendipalm"]["years"] = years

        elif header == "SPCL Smallholders":

            structure["projects"]["SPCL Smallholders"] = {
                "column": col,
                "years": years,
            }

        elif header == "Tanoobia Smallholders":

            structure["projects"]["Tanoobia Smallholders"] = {
                "column": col,
                "years": years,
            }

        # Ignore total columns we don't use
        elif header in [
            "TOTAL Smallholders",
            "DAF Smallholders",
            "DAF Serendipalm",
            "TOTAL DAF",
        ]:
            pass

        # Everything else before the totals is a Serendipalm estate
        else:

            structure["projects"]["Serendipalm"]["locations"][header] = {
                "column": col,
                "years": years,
            }

        col += 3

    return structure


# ============================================================
# YEAR -> COLUMN
# ============================================================

def get_column(base_column, year):

    offsets = {
        2026: 0,
        2025: 1,
        2024: 2,
    }

    return base_column + offsets[int(year)]


# ============================================================
# METRIC LOOKUP
# ============================================================

def get_metric(sheet, metric_name, column):

    for row in range(1, sheet.max_row + 1):

        if clean(sheet.cell(row=row, column=1).value) == metric_name:

            return sheet.cell(row=row, column=column).value

    return None


# ============================================================
# LIST METRICS
# ============================================================

def list_metrics(sheet):

    metrics = []

    for row in range(1, sheet.max_row + 1):

        value = clean(sheet.cell(row=row, column=1).value)

        if value != "":
            metrics.append(value)

    return metrics
