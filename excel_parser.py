"""
excel_parser.py

Parses the SPCL dashboard workbook into structures
used by the Streamlit dashboard.
"""

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

STOP_HEADERS = [
    "DAF Smallholders",
    "DAF Serendipalm",
    "TOTAL DAF",
]

SMALLHOLDER_HEADERS = [
    "SPCL Smallholders",
    "Tanoobia Smallholders",
]


def agriculture_structure(sheet):

    structure = {
        "projects": {
            "Serendipalm": {
                "column": None,
                "years": [],
                "locations": {}
            },
            "SPCL Smallholders": {},
            "Tanoobia Smallholders": {},
            "All Projects": {}
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
        # Serendipalm locations
        # --------------------------------------------

        if header in [
            "Tweapease",
            "Abaam",
            "SWARF",
            "Old Cassava (other name?)",
            "Fante-Onomabo",
        ]:

            structure["projects"]["Serendipalm"]["locations"][header] = {
                "column": col,
                "years": years,
            }

        # --------------------------------------------
        # Smallholders
        # --------------------------------------------

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

        # --------------------------------------------
        # Workbook totals
        # --------------------------------------------

        elif header == "TOTAL Smallholders":

            structure["projects"]["Smallholders Total"] = {
                "column": col,
                "years": years,
            }

        elif header == "TOTAL Serendipalm":

            structure["projects"]["Serendipalm"]["column"] = col
            structure["projects"]["Serendipalm"]["years"] = years

        elif header == "TOTAL All Locations":

            structure["projects"]["All Projects"] = {
                "column": col,
                "years": years,
            }

            break

        col += 3

    return structure


# ------------------------------------------------------------------
# Metric Lookup
# ------------------------------------------------------------------

def get_metric(sheet, metric_name, column):

    for row in range(1, sheet.max_row + 1):

        value = clean(
            sheet.cell(row=row, column=1).value
        )

        if value == metric_name:

            return sheet.cell(
                row=row,
                column=column
            ).value

    return None


# ------------------------------------------------------------------
# Agriculture Year -> Column
# ------------------------------------------------------------------

def get_column(base_column, year):

    year_map = {
        2026: 0,
        2025: 1,
        2024: 2,
    }

    if year not in year_map:
        return None

    return base_column + year_map[year]


# ------------------------------------------------------------------
# List Metrics
# ------------------------------------------------------------------

def list_metrics(sheet):

    metrics = []

    for row in range(1, sheet.max_row + 1):

        value = clean(
            sheet.cell(row=row, column=1).value
        )

        if value != "":
            metrics.append(value)

    return metrics


# ==================================================================
# SOCIAL
# ==================================================================

# ------------------------------------------------------------------
# Social Employee Data
# ------------------------------------------------------------------

def social_employee_data(sheet):

    """
    Reads the Serendipalm Employees table.

    Source:
        Social!A5:K12

    Columns:
        A = Employee Type
        B-F = Male 2026-2022
        G-K = Female 2026-2022

    Returns a dictionary organized by year.
    """

    years = [
        2026,
        2025,
        2024,
        2023,
        2022,
    ]

    employee_types = [
        "Managerial",
        "Non-Managerial",
        "Temporary",
        "Piece Rate",
        "Total",
    ]

    data = {}

    for year_index, year in enumerate(years):

        male_column = 2 + year_index
        female_column = 7 + year_index

        data[year] = []

        for row in range(8, 13):

            employee_type = clean(
                sheet.cell(row=row, column=1).value
            )

            if employee_type not in employee_types:
                continue

            male = sheet.cell(
                row=row,
                column=male_column
            ).value

            female = sheet.cell(
                row=row,
                column=female_column
            ).value

            data[year].append({
                "Type": employee_type,
                "Male": male if male is not None else 0,
                "Female": female if female is not None else 0,
            })

    return data


# ------------------------------------------------------------------
# Fair Trade Premium Data
# ------------------------------------------------------------------

def social_fair_trade_data(sheet):

    """
    Reads the Fair Trade Premium Spending table.

    Source:
        Social!A15:K23

    Columns:
        A = Spending Category
        B-K = 2026-2017

    Returns a dictionary organized by year.
    """

    years = [
        2026,
        2025,
        2024,
        2023,
        2022,
        2021,
        2020,
        2019,
        2018,
        2017,
    ]

    categories = [
        "Farmer Support",
        "Health",
        "Education",
        "Water & Sanitation",
        "Infrastructure",
        "Other",
        "Total",
    ]

    data = {}

    for year_index, year in enumerate(years):

        column = 2 + year_index

        data[year] = []

        for row in range(17, 24):

            category = clean(
                sheet.cell(row=row, column=1).value
            )

            if category not in categories:
                continue

            value = sheet.cell(
                row=row,
                column=column
            ).value

            # Treat blanks and "-" as zero for dashboard calculations
            if value is None:
                value = 0

            if isinstance(value, str):
                if value.strip() in ["-", "–", "—"]:
                    value = 0
                else:
                    try:
                        value = float(value.replace(",", ""))
                    except ValueError:
                        value = 0

            data[year].append({
                "Category": category,
                "Amount": value,
            })

    return data
