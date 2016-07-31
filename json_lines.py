import csv
import re
import json


i = 0

out_file = open('fixed_ts.json', 'wb')
with open('fixed_ts.csv', 'rb') as csvfile:
    sr_reader = csv.reader(csvfile)
    for row in sr_reader:
        j = {
            #RequestNum, Status, DateEntere, DateReceiv, DateRespon, DateComple, DateDue, RequestTyp, IncidentAd, FMTD_TITLE, latitude, longitude
            "request_num": row[0],
            "request_status": row[1],
            "timestamp": row[2],
            "ts2": row[3],
            "ts3": row[4],
            "ts4": row[5],
            "ts5": row[6],
            "service_request": row[7],
            "address": row[8],
            "lot_no": row[9],
            "geoip": {
                "latitude": row[10],
                "longitude": row[11]
            }
        }
        #"lat": row[10],
        #"long": row[11]
        #}
        out_file.writelines([json.dumps(j) + "\r\n"])
        i+=1

        if i > 5:
            break
out_file.close()