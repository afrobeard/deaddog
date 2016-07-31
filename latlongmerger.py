import csv
import re

"""
def generate_address_lookup_dict():
    d = {}
    with open('parcel_points.csv', 'rb') as csvfile:
        address_lookup_reader = csv.reader(csvfile)
        for row in address_lookup_reader:
            (_, house_no, street, suburb, lot_no, fmtd_address, latitude, longitude) = tuple(row)
            if suburb:

                if suburb in d:
                    pass
                else:
                    d[suburb] = []
                d[suburb].append((lot_no, fmtd_address, latitude, longitude))
    return d

ADDRESS_LOOKUP_TABLE = generate_address_lookup_dict()

def address_lookup(lot_number, street_address, suburb, state, postcode):
    lookup_key = " ".join([suburb, state, postcode])
    li = ADDRESS_LOOKUP_TABLE.get(lookup_key)

    if li:
        street_address_li = street_address.split()
        for x in li:
            count = 0
            for item in street_address_li:
                if item in li[1]:
                    count += 1
            print 1.0 * count / len(street_address_li)


        print ">>", lot_number, street_address, lookup_key
        print ">>>", li[0]
        #print repr(li)
        print ">>>>", repr([x for x in li if street_address in li[1]])
        exit(0)


    if li:
        print len(li)
    else:
        print repr(li)
    return len(li)
"""

import urllib
import urllib2
import json


def address_lookup(lot_number, street_address, suburb, state, postcode):

    lookup_address = " ".join([street_address, suburb, state, postcode])
    params = urllib.urlencode({
        "address": lookup_address,
        "key": "AIzaSyDSoz6Vg-VFjKHl86Nz5OHsLUBgbsWidFE"
    }, True)
    prefix = "https://maps.googleapis.com/maps/api/geocode/json?"
    path = prefix + params
    f = urllib2.urlopen(prefix + params)
    data = f.read()
    d = json.loads(data)
    lat_lng = d["results"][0]["geometry"]["location"]
    return(lat_lng.get('lat'), lat_lng.get('lng'))



def parse_address(address_raw, lot_raw):
    """
    Address raw looks like -> 2 Alma Street RYDALMERE NSW 2116
    Lot raw looks like -> Lot 189 DP15160

    :param address_raw:
    :param lot_raw:
    :return:
    """
    lot_number = None

    address_raw_parts = address_raw.split()

    if len(address_raw_parts) < 4:
        return None

    postcode = address_raw_parts[-1]
    state = address_raw_parts[-2]
    suburb = address_raw_parts[-3]
    street_address = " ".join(address_raw_parts[:-3])

    lot_match = re.match("Lot (\w+)", lot_raw)
    if lot_match:
        lot_number = lot_match.groups()[0]

    return (lot_number, street_address, suburb, state, postcode)


out_file = open('service_requests_lat_lng.csv', 'wb')
csv_writer = csv.writer(out_file)


with open('service_requests.csv', 'rb') as csvfile:
    sr_reader = csv.reader(csvfile)
    for row in sr_reader:
        #print(repr(row))
        """
        ['176332',
         'Request Completed',
         '1/1/2016, 10:07:16 PM',
         '1/1/2016, 10:07:57 PM',
         '1/6/2016, 2:24:10 AM',
         '1/6/2016, 2:24:10 AM',
         '1/6/2016, 10:07:57 PM',
         'Waste Bin Damaged',
         '10 Morshead Crescent SOUTH GRANVILLE NSW 2142',
         'Lot 20 DP35670']
         """
        try:
            (sr_id, sr_status, sr_ts1, sr_ts2, sr_ts3, sr_ts4, st_ts5, sr_service_request_text, sr_address_raw, sr_lot_raw) = \
                (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
            (sr_lot_number, sr_street_address, sr_suburb, sr_state, sr_postcode) = \
                parse_address(sr_address_raw, sr_lot_raw)
            #print(repr((sr_lot_number, sr_street_address, sr_suburb, sr_state, sr_postcode)))
            (sr_lat, sr_lng) = address_lookup(sr_lot_number, sr_street_address, sr_suburb, sr_state, sr_postcode)
            csv_writer.writerow([sr_id, sr_status, sr_ts1, sr_ts2, sr_ts3, sr_ts4, st_ts5, sr_service_request_text, sr_address_raw,
                   sr_lot_raw, sr_lat, sr_lng])
        except Exception, e:
            #raise e
            continue

