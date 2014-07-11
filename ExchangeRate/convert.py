from datetime import datetime
import os
import re
import json
import sys
import shutil
from DB import DB
from DB import extractions
from DB import bankLogs

path = "/home/exchangerate/ExchangeRate/ExchangeRate/output/"
outpath = "/home/exchangerate/ExchangeRate/ExchangeRate/output/convert2mysql/"
print "get filelist in '%s'" % path
paths = [os.path.join(path,fn) for fn in next(os.walk(path))[2]]
print "...got %d files" % len(paths)

print "sort files"
paths.sort()
print "...sorted"

print "connect to DB"
DB_USER = os.environ['EXCHANGERATE_DB_USER']
DB_PASS = os.environ['EXCHANGERATE_DB_PASS']
DB_DATABASE = os.environ['EXCHANGERATE_DB_DATABASE']

print "connect to DB"
db = DB.DB(username=DB_USER, password=DB_PASS, database=DB_DATABASE)
extr = extractions(db)
bankLogs = bankLogs(db)
print "...connected"

print "start loop"
print ""
for path in paths:
    filename = os.path.basename(path)
    m = re.search("\/(?P<date>[0-9]{8}-[0-9]{6})-(?P<bank>[A-Za-z0-9_]+)\.json$", path)
    dt = datetime.strptime(m.group('date'), '%Y%m%d-%H%M%S')
    bank = m.group('bank')
    #print path
    sys.stdout.write("\r    %s - %-20s" % (dt, bank))
    sys.stdout.flush()
    
    data = None
    try:
        json_data = open(path)
        data = json.load(json_data)
        json_data.close()
    except ValueError:
        bankLogs.insert(bank, "json:loadFailed", dt)
        print "Cannot load json from %s" % (path)
    
    if data:
        for curr in data[0]:
            m = re.search("^(?P<currency>[A-Z]{3})_(?P<optype>.+)$", curr)
            #print "%s %s %s" % (m.group('currency'), m.group('optype'), float(data[0][curr]))
            extr.insert(bank, m.group('optype'), m.group('currency'), float(data[0][curr]), dt)
            
        bankLogs.insert(bank, "data:inserted", dt)
        extr.commit()

    bankLogs.commit()
    shutil.move(path, outpath+filename)
