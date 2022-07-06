import time
import schedule
from application.exporter import exporter
from worker import work


@schedule.repeat(schedule.every().thursday.at('03:15'))
def get_metrics_week():
    exporter('msk-sch', 'week2')


@schedule.repeat(schedule.every().thursday.at('05:10'))
def get_metrics_week():
    exporter('sergpas', 'week2')


@schedule.repeat(schedule.every().thursday.at('04:15'))
def get_metrics_week():
    exporter('south', 'week2')


@schedule.repeat(schedule.every().thursday.at('11:00'))
def get_metrics_week():
    exporter('vkus', 'week2')


@schedule.repeat(schedule.every().thursday.at('01:15'))
def get_metrics_week():
    exporter('omsk', 'week2')
    
    
@schedule.repeat(schedule.every().thursday.at('06:10'))
def get_metrics_week():
    exporter('veris', 'week2')


@schedule.repeat(schedule.every().thursday.at('00:15'))
def get_metrics_week():
    exporter('korsakov', 'week2')


@schedule.repeat(schedule.every().thursday.at('07:10'))
def get_metrics_week():
    exporter('vkz', 'week2')


@schedule.repeat(schedule.every().day.at('14:09'))
def get_metrics_week():
    exporter('zelen', 'week2')


@schedule.repeat(schedule.every().day.at('14:10'))
def get_metrics_day():
    work('zelen', 'week2')


@schedule.repeat(schedule.every().thursday.at('03:30'))
def get_metrics_day():
    work('msk-sch', 'week2')


@schedule.repeat(schedule.every().thursday.at('05:15'))
def get_metrics_day():
    work('sergpas', 'week2')


@schedule.repeat(schedule.every().thursday.at('04:30'))
def get_metrics_day():
    work('south', 'week2')


@schedule.repeat(schedule.every().thursday.at('11:30'))
def get_metrics_day():
    work('vkus', 'week2')


@schedule.repeat(schedule.every().thursday.at('01:30'))
def get_metrics_day():
    work('omsk', 'week2')
    
    
@schedule.repeat(schedule.every().thursday.at('06:15'))
def get_metrics_day():
    work('veris', 'week2')


@schedule.repeat(schedule.every().thursday.at('00:25'))
def get_metrics_day():
    work('korsakov', 'week2')


@schedule.repeat(schedule.every().thursday.at('07:15'))
def get_metrics_day():
    work('vkz', 'week2')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
