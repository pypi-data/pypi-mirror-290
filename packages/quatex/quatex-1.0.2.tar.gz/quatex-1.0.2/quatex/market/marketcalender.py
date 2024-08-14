import datetime as dt

import pandas_market_calendars as cal

holidays = set()
nyse = cal.get_calendar('NYSE')
for holiday in nyse.holidays().holidays:
    holidays.add(holiday.astype(dt.date))


def is_holiday(date: dt.date):
    weekday = date.isoweekday()
    return weekday == 6 or weekday == 7 or (date in holidays)
