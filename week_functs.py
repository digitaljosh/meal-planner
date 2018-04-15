import datetime


def get_today_string():
    today_string = "{date:%m/%d}".format(date=datetime.datetime.now())
    return today_string

def get_week_from_string():
    today = datetime.datetime.today()
    week_from_date = today + datetime.timedelta(days=7)
    week_from = "{date:%m/%d}".format(date=week_from_date)
    return week_from

