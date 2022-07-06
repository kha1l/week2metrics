from postgres.psql import Database
from orders.export import DataExportDay
from date_work import DataWork
import time
from datetime import date


def exporter(group: str, tps: str):
    db = Database()
    dt = DataWork(date_end=date(2022, 6, 29)).set_date()
    users = db.get_users(group)
    for user in users:
        data = DataExportDay(dt, user[0], tps)
        data.losses()
        time.sleep(10)
