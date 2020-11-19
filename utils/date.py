import datetime


# 暂时不考虑超过一天的情况
def hhmmss2secs(hhmmss: str):
    if hhmmss:
        parts = hhmmss.split(':')
        hours = int(parts[0]) if parts[0] else 0
        minutes = int(parts[1]) if parts[1] else 0
        secs = int(parts[2]) if parts[2] else 0
        return hours * 3600 + minutes * 60 + secs
    else:
        return 0


def plus_hhmmss(hhmmss1: str, hhmmss2: str):
    secs1 = hhmmss2secs(hhmmss1)
    secs2 = hhmmss2secs(hhmmss2)
    return str(datetime.timedelta(seconds=secs1 + secs2))
