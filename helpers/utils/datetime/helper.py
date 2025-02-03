import datetime
import zoneinfo

TAIWAN_TIMEZONE = zoneinfo.ZoneInfo("Asia/Taipei")


def datetime_now() -> datetime.datetime:
    return datetime.datetime.now(tz=TAIWAN_TIMEZONE)
