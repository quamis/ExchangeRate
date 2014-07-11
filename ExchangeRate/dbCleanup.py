import mysql.connector
from datetime import datetime
import os
import re
import json
import sys
import shutil
from database import db
from database import extractions
from database import bankLogs


DB_USER = os.environ['EXCHANGERATE_DB_USER']
DB_PASS = os.environ['EXCHANGERATE_DB_PASS']
DB_DATABASE = os.environ['EXCHANGERATE_DB_DATABASE']

print "connect to DB"
db = db.db(username=DB_USER, password=DB_PASS, database=DB_DATABASE)
extr = extractions.extractions(db)
bankLogs = bankLogs.bankLogs(db)
print "...connected"

availableBanks = extr.db.getCol("SELECT DISTINCT `bank` FROM `extractions` ORDER BY `bank`")
print availableBanks

availableCurrencies = extr.db.getCol("SELECT DISTINCT `currency` FROM `extractions` ORDER BY `currency`")
print availableCurrencies

for bank in availableBanks:
    for currency in availableCurrencies:
        types = ['buy', 'sell']
        for op in types:
            print "Cleanup records for %s, %s %s" % (bank, op, currency)
            records = extr.db.getQueryCursor("SELECT `id`, `value` FROM `extractions` WHERE `bank`=%s AND `type`=%s AND `currency`=%s ORDER BY `time` ASC", [bank, op, currency])

            lextrvalue= 0.0

            stat_total = 0
            stat_same = 0
            cleanupIds = []
            for (extrid, extrvalue) in records:
                same = False
                stat_total+=1
                if lextrvalue==extrvalue:
                    same = True
                    
                if same:
                    stat_same+=1
                    cleanupIds.append(extrid)
                    
                lextrvalue=extrvalue
            extr.db.closeQueryCursor(records)
            
            print "... done. Should delete %d from %d records" % (stat_same, stat_total)
            print "start cleanup"
            for cid in cleanupIds:
                extr.db.execute("DELETE FROM `extractions` WHERE `id`=%s", [cid])
            extr.db.commit()
            print "...done"   
    
    