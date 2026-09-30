"""
Parses the SPCL dashboard workbooks into structures used by Streamlit.
"""


def clean(value):
    if value is None:
        return ""
    return str(value).strip()


def number(value):
    """Convert workbook values to numbers, treating blanks/dashes as zero."""
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value in ["", "-", "–", "—"]:
            return 0
        try:
            return float(value.replace(",", ""))
        except ValueError:
            return 0
    return 0


# ==================================================================
# AGRICULTURE
# ==================================================================

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


def get_metric(sheet, metric_name, column):
    for row in range(1, sheet.max_row + 1):
        value = clean(sheet.cell(row=row, column=1).value)
        if value == metric_name:
            return sheet.cell(row=row, column=column).value
    return None


def get_column(base_column, year):
    year_map = {
        2026: 0,
        2025: 1,
        2024: 2,
    }
    if year not in year_map:
        return None
    return base_column + year_map[year]


def list_metrics(sheet):
    metrics = []
    for row in range(1, sheet.max_row + 1):
        value = clean(sheet.cell(row=row, column=1).value)
        if value != "":
            metrics.append(value)
    return metrics


# ==================================================================
# SOCIAL — separate SPCL_SocialData_Input.xlsx workbook
# ==================================================================

def social_employee_data(sheet):
    """
    Read the row-based Employees worksheet.

    Columns beginning at row 7:
        A = Year
        B = Role Type
        C = Employee Type (Male/Female)
        D = Number of Employees
    """
    role_types = [
        "Managerial",
        "Non-Managerial",
        "Temporary",
        "Piece Rate",
    ]

    grouped = {}

    for row in range(7, sheet.max_row + 1):
        year_value = sheet.cell(row=row, column=1).value
        role = clean(sheet.cell(row=row, column=2).value)
        gender = clean(sheet.cell(row=row, column=3).value)
        count = number(sheet.cell(row=row, column=4).value)

        if not isinstance(year_value, (int, float)):
            continue
        if role not in role_types or gender not in ["Male", "Female"]:
            continue

        year = int(year_value)
        grouped.setdefault(
            year,
            {item: {"Male": 0, "Female": 0} for item in role_types}
        )
        grouped[year][role][gender] += count

    data = {}

    for year, roles in grouped.items():
        data[year] = []
        total_male = 0
        total_female = 0

        for role in role_types:
            male = roles[role]["Male"]
            female = roles[role]["Female"]
            total_male += male
            total_female += female
            data[year].append({
                "Type": role,
                "Male": male,
                "Female": female,
            })

        data[year].append({
            "Type": "Total",
            "Male": total_male,
            "Female": total_female,
        })

    return data


def social_fair_trade_data(sheet):
    """
    Read the row-based FTP worksheet.

    Columns beginning at row 7:
        A = Year
        B = Project Type
        C = Total Amount
    """
    categories = [
        "Farmer Support",
        "Health",
        "Education",
        "Water & Sanitation",
        "Infrastructure",
        "Other",
    ]

    grouped = {}

    for row in range(7, sheet.max_row + 1):
        year_value = sheet.cell(row=row, column=1).value
        category = clean(sheet.cell(row=row, column=2).value)
        amount = number(sheet.cell(row=row, column=3).value)

        if not isinstance(year_value, (int, float)):
            continue
        if category not in categories:
            continue

        year = int(year_value)
        grouped.setdefault(year, {item: 0 for item in categories})
        grouped[year][category] += amount

    data = {}

    for year, spending in grouped.items():
        data[year] = [
            {"Category": category, "Amount": spending[category]}
            for category in categories
        ]
        data[year].append({
            "Category": "Total",
            "Amount": sum(spending.values()),
        })

    return data
