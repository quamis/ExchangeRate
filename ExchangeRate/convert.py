#!/usr/bin/python
from datetime import datetime
import os, errno
import re
import json
import sys
import shutil
from database import db
from database import extractions
from database import bankLogs

import argparse

parser = argparse.ArgumentParser(description='Convert json files to mysql rows. You must have the mysql params in the environment.')
parser.add_argument('--input', dest='input',            action='store',         type=str,   help='must end in "/"')
parser.add_argument('--output', dest='output',          action='store',         type=str,   help='must end in "/"')
parser.add_argument('--commitType', dest='commitType',          action='store', type=str,   default='often', help='Can be: often, daily, once')
args = vars(parser.parse_args())

pathinput = args['input']
pathoutput = args['output']

print "get filelist in '%s'" % pathinput
paths = [os.path.join(pathinput,fn) for fn in next(os.walk(pathinput))[2]]
print "...got %d files" % len(paths)

print "sort files"
paths.sort()
print "...sorted"

print "grab env variables"
DB_USER = os.environ['EXCHANGERATE_DB_USER']
DB_PASS = os.environ['EXCHANGERATE_DB_PASS']
DB_DATABASE = os.environ['EXCHANGERATE_DB_DATABASE']

print "connect to DB"
db = db.db(username=DB_USER, password=DB_PASS, database=DB_DATABASE)
extr = extractions.extractions(db)
bankLogs = bankLogs.bankLogs(db)
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
        if args['commitType']=='often':
            extr.commit()

    if args['commitType']=='often':
        bankLogs.commit()
    
    subdir = dt.strftime("%Y%m%d")+"/"
    
    try:
        os.mkdir(pathoutput+subdir)
        if args['commitType']=='daily':
            extr.commit()
            bankLogs.commit()
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        
    shutil.move(path, pathoutput+subdir+filename)

if args['commitType']=='once':
    extr.commit()
    bankLogs.commit()
    
extr.commit()
bankLogs.commit()