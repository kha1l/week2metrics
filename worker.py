from postgres.psql import Database
from application.reader import Reader
from application.changer import Changer
from date_work import DataWork
from datetime import timedelta, date


def work(group: str, tps: str):
    db = Database()
    users = db.get_users(group)
    dt = DataWork(date_end=date(2022, 6, 29)).set_date()
    for user in users:
        if tps == 'week2':
            line = db.get_line(dt - timedelta(days=3), user[0])
        else:
            line = db.get_line(dt, user[0])
        cls_df = Reader(user[0], tps)
        cls_df.read_df()
        change = Changer(cls_df)
        los, scr, unc, prep = change.change_losses()
        rp, avg_rp, st, avg_st = change.change_orders(user[0])
        if len(line) != 0:
            db.update_week2_metrics(dt - timedelta(days=3), user[0], los, scr, unc, prep, rp, avg_rp, st, avg_st)
        else:
            db.add_week2_metrics(dt - timedelta(days=3), user[0], user[1], los, scr, unc, prep, rp, avg_rp, st, avg_st)
        print(user[0])
