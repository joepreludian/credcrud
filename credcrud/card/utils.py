from datetime import datetime, timedelta


def standardize_expire_date(expire_date: str) -> str:
    expire_date_obj = datetime.strptime(expire_date, "%m/%Y")

    next_month = expire_date_obj.replace(day=1, month=expire_date_obj.month + 1)
    last_day_of_month = (next_month - timedelta(days=1)).day

    formatted_date = expire_date_obj.strftime("%Y-%m-{:02d}".format(last_day_of_month))
    return formatted_date


def format_standard_date_to_expire_date(standardized_expire_date) -> str:
    return datetime.strptime(standardized_expire_date, "%Y-%m-%d").strftime("%m/%Y")
