from datetime import datetime

def safe_parse_datetime(date_str: str, time_str: str) -> datetime:
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        time = datetime.strptime(time_str, "%H:%M").time()
    except ValueError:
        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
        time = datetime.strptime(time_str, "%H:%M:%S").time()
    return datetime.combine(date, time)