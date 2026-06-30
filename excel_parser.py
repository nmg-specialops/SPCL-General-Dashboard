# excel_parser.py

EXCLUDED_HEADERS = {
    "TOTAL Smallholders",
    "TOTAL Serendipalm",
    "DAF Smallholders",
    "DAF Serendipalm",
    "TOTAL DAF",
    "TOTAL All Locations",
}


def agriculture_structure(sheet):
    """
    Reads the Agriculture sheet and returns a structure
    describing Projects, Locations and Years.
    """

    data = {
        "Serendipalm": {},
        "SPCL Smallholders": {},
        "Tanoobia Smallholders": {}
    }

    col = 2

    while col <= sheet.max_column:

        header = sheet.cell(row=6, column=col).value

        if header is None:
            col += 1
            continue

        # Ignore reporting columns
        if header in EXCLUDED_HEADERS:
            break

        years = []

        for offset in range(3):
            years.append(sheet.cell(row=7, column=col + offset).value)

        if header == "SPCL Smallholders":

            data["SPCL Smallholders"] = {
                "column": col,
                "years": years
            }

        elif header == "Tanoobia Smallholders":

            data["Tanoobia Smallholders"] = {
                "column": col,
                "years": years
            }

        else:

            data["Serendipalm"][header] = {
                "column": col,
                "years": years
            }

        col += 3

    return data
