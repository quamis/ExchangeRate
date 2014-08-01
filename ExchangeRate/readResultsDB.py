#!/usr/bin/python
import os, sys, re, json, datetime
import collections
from database import db
from database import extractions
from database import bankLogs

import argparse

parser = argparse.ArgumentParser(description='Print composed data')
parser.add_argument('--format', dest='format',          action='store',         type=str,   default="linear",           help='TODO')
parser.add_argument('-f',       dest='file',            action='store',         type=str,   default=None,               help='TODO')
parser.add_argument('-days',    dest='days',            action='store',         type=float,   default=int(3*30.5),               help='TODO')
args = vars(parser.parse_args())


DB_USER = os.environ['EXCHANGERATE_DB_USER']
DB_PASS = os.environ['EXCHANGERATE_DB_PASS']
DB_DATABASE = os.environ['EXCHANGERATE_DB_DATABASE']

print "connect to DB"
db = db.db(username=DB_USER, password=DB_PASS, database=DB_DATABASE)
extr = extractions.extractions(db)
bankLogs = bankLogs.bankLogs(db)
print "...connected"

availableBanks = extr.db.getCol("SELECT DISTINCT `bank` FROM `extractions` ORDER BY `bank`")
#print availableBanks

availableCurrencies = extr.db.getCol("SELECT DISTINCT `currency` FROM `extractions` ORDER BY `currency`")
#print availableCurrencies

startTime = datetime.date.today()
startTime = startTime-datetime.timedelta(days=args['days'])
rawData = extr.db.getAll("SELECT * FROM `extractions` WHERE `time`>%s", keys = ('id', 'bank', 'type', 'time', 'currency', 'value'), params=[startTime])
#print rawData

if args['format']=='groupedByTimeAndCurrencyAndBank':
    fullData = collections.OrderedDict()
    for d in rawData:
        if d['time'] not in fullData:
            fullData[d['time']] = {}

        if d['currency'] not in fullData[d['time']]:
            fullData[d['time']][d['currency']] = {}

        if d['bank'] not in fullData[d['time']][d['currency']]:
            fullData[d['time']][d['currency']][d['bank']] = {}
            
        fullData[d['time']][d['currency']][d['bank']][d['type']] = d['value']
    
    if args['file']:
        f = open(args['file'], "w")
        f.write(json.dumps(fullData))
        f.close()
    else:
        print json.dumps(fullData)
        
elif args['format']=='linear':
    fullData = []
    for d in rawData:
        r = {}
        r['time'] = d['time'].isoformat()
        r['bank'] = d['bank']
        r['type'] = d['type']
        r['currency'] = d['currency']
        r['value'] = d['value']
        fullData.append(r)
        
    if args['file']:
        f = open(args['file'], "w")
        f.write("ExchangeRateData = "+json.dumps(fullData)+";")
        f.close()
    else:
        print json.dumps(fullData)

