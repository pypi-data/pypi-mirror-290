from datetime import datetime, date

def jayna_birfday():
    today = date.today()
    current_year = today.year
    next_april_29 = date(current_year, 4, 29)

    if today > next_april_29:
        next_april_29 = date(current_year + 1, 4, 29)

    days_remaining = (next_april_29 - today).days
    return f"There are {days_remaining} days remaining until the most wonderful day of the year (jayna birthday!!)"