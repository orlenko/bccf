import datetime
import logging
import time

from dateutil import rrule


log = logging.getLogger(__name__)


def quarter(month):
    return (month - 1) // 3 + 1


def quarters():
    START_DATE = datetime.datetime(2013, 9, 1)
    retval = []
    range_end = datetime.datetime.utcnow()
    rule = rrule.rrule(rrule.MONTHLY,
                       bymonth=(1,4,7,10),
                       bysetpos=-1,
                       dtstart=datetime.datetime(range_end.year - 10, 1, 1))
    for _i in range(6):
        range_start = rule.before(range_end, inc=1)
        if START_DATE < range_start:
            item_id = 'okr_%s' % int(datetime_to_timestamp(range_start))
            label = 'Q%s %s' % (quarter(range_start.month), range_start.year)
            retval.append({
                'id': item_id,
                'name': label
            })
        range_end = range_start - datetime.timedelta(1)
    log.debug('Quarters: %s' % retval)
    return retval


def quarter_boundaries(quarter_start_seconds):
    range_start = datetime.datetime.utcfromtimestamp(int(quarter_start_seconds))
    rule = rrule.rrule(rrule.MONTHLY,
                       bymonth=(1,4,7,10),
                       bysetpos=-1,
                       dtstart=range_start)
    return range_start, rule.after(range_start + datetime.timedelta(1), inc=1)


def timedelta_to_float(delta):
    return float(delta.days * 60 * 60 * 24
                + delta.seconds
                + delta.microseconds / 1000000.0)


def datetime_to_timestamp(dt):
    if dt is None:
        return None

    if dt.tzinfo:
        reference = datetime.datetime.fromtimestamp(0, dt.tzinfo)
    else:
        reference = datetime.datetime.utcfromtimestamp(0)
    retval = timedelta_to_float(dt - reference)
    if time.localtime(retval)[8]:
        retval -= 60 * 60
    return retval


def get_start_of_day_sec(timestamp):
    locTime = time.localtime(timestamp)
    locTimeStartOfDay = tuple(locTime[:3] + (0,)*3 + locTime[-3:])
    return time.mktime(locTimeStartOfDay)


def get_start_of_day_datetime(dt):
    sec = get_start_of_day_sec(datetime_to_timestamp(dt))
    return datetime.datetime.fromtimestamp(sec)
