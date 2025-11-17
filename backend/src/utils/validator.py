from dateutil import parser
from datetime import datetime, timedelta

class Validator:
    def validate_date(self, date_str):
        try:
            dt = parser.parse(date_str, fuzzy=True).date()
            return dt if dt >= datetime.now().date() - timedelta(days=7) else None
        except:
            return None

    def validate_time(self, time_str):
        try:
            dt = datetime.strptime(time_str, "%H:%M")
            return dt.strftime("%H:%M")
        except:
            return None

validator = Validator()
