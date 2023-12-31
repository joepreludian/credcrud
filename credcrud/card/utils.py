from datetime import date, datetime, timedelta


def expire_date_to_date(expire_date: str) -> date:
    expire_date_obj = datetime.strptime(expire_date, "%m/%Y")
    next_month = expire_date_obj.replace(day=1, month=expire_date_obj.month + 1)
    return (next_month - timedelta(days=1)).date()


def date_to_expire_date(date: date) -> str:
    return date.strftime("%m/%Y")
