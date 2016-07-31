import csv
import re
import urllib
import urllib2
import json
import dateparser
import datetime
import time

def to_unix_ts(str_ts):
    ts = ""
    if str_ts:
        str_ts = str_ts.strip()
        if str_ts:
            try:
                print str_ts
                dt = dateparser.parse(str_ts)
                ts = time.mktime(dt.timetuple())
            except:
                pass
    ts = str(ts)
    print ts
    return ts

out_file = open('fixed_ts.csv', 'wb')
csv_writer = csv.writer(out_file)

with open('fixed.csv', 'rb') as csvfile:
    sr_reader = csv.reader(csvfile)
    for row in sr_reader:
        if True:
            (ts1, ts2, ts3, ts4, ts5) = (row[2], row[3], row[4], row[5], row[6])
            (ts1, ts2, ts3, ts4, ts5) = (to_unix_ts(ts1), to_unix_ts(ts2), to_unix_ts(ts3), to_unix_ts(ts4), to_unix_ts(ts5))
            (row[2], row[3], row[4], row[5], row[6]) = (ts1, ts2, ts3, ts4, ts5)
            print repr(row)
            csv_writer.writerow(row)
        #except Exception, e:
        #    #raise e
        #    continue
        pass
