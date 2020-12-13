import datetime as dt

d1 = dt.timedelta(hours=3)
d2 = dt.timedelta(hours=5)
print((d2 - d1) // dt.timedelta(minutes=10))