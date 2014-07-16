#!/usr/bin/python
import os, sys, re, json
import collections
import argparse
import datetime
from termcolor import colored, cprint

parser = argparse.ArgumentParser(description='Print composed data')
parser.add_argument('--output', dest='output',          action='store',         type=str,   default="print",            help='TODO')
parser.add_argument('-f',       dest='file',            action='store',         type=str,   default=None,               help='TODO')

parser.add_argument('--management-hide',dest='management_hide', action='store_true',        default=False,              help='TODO')

parser.add_argument('--print-diff',     dest='print_diff',      action='store_true',        default=False,              help='TODO')
parser.add_argument('--print-bank',     dest='print_bank',      action='append',            default=None,               help='TODO')
parser.add_argument('--print-operation',dest='print_operation', action='append',            default=None,               help='TODO')
parser.add_argument('--print-days',     dest='print_days',      action='store',  type=int,  default=3,                  help='TODO')
parser.add_argument('--print-currency', dest='print_currency',  action='append', type=str,  default=None,               help='TODO')
args = vars(parser.parse_args())

if args['print_operation'] is None:
    args['print_operation'] = [ 'sell', 'buy' ]
    
FOLDER="output/"
jsonFiles=[]
for filename in os.listdir(FOLDER):
    jsonFiles.append(filename)

jsonFiles.sort()

fullData = collections.OrderedDict()
fullCurrencies = None
lastFiles = {}
for file in jsonFiles:
    matches = re.search("[0-9]{6}-(?P<bank>[A-Za-z]+)\.json$", file)
    if matches is None:
        continue
        
    bank = matches.group('bank')
        
    try:
        json_data = open(FOLDER+file)
        data = json.load(json_data)
        json_data.close()
        
        lastFiles[bank] = file
    except ValueError:
        if bank in lastFiles:
            print "Cannot load json from %s. Assume last values for %s from %s" % (file, bank, lastFiles[bank])
            json_data = open(FOLDER+lastFiles[bank])
            data = json.load(json_data)
            json_data.close()
        else:
            print "No history for %s" % (bank)
    
    matches = re.match("^(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})-(?P<hour>[0-9]{2})(?P<minute>[0-9]{2})(?P<second>[0-9]{2})-(?P<system>.+).json$", file)
    key= "%s-%s-%s %s:%s:%s" % (matches.group('year'), matches.group('month'), matches.group('day'), matches.group('hour'), matches.group('minute'), matches.group('second'))
    if not key in fullData:
        fullData[key] = { }
        fullData[key]['date'] = "%s-%s-%sT%s:%s:%s+0000" % (matches.group('year'), matches.group('month'), matches.group('day'), matches.group('hour'), matches.group('minute'), matches.group('second'))
        fullData[key]['values'] = { }
    
    rawValuesCurrencies = data[0]
    valuesGroupedByCurrencies = {}
    for curr in rawValuesCurrencies:
        mc = re.match("^(?P<currency>[A-Z]+)_(?P<operation>.+)", curr)
        
        if not mc.group('currency') in valuesGroupedByCurrencies:
            valuesGroupedByCurrencies[mc.group('currency')] = {}
        
        valuesGroupedByCurrencies[mc.group('currency')][mc.group('operation')] = rawValuesCurrencies[curr]
            
    fullData[key]['values'][matches.group('system')] = valuesGroupedByCurrencies
    
    if fullCurrencies is None:
        fullCurrencies = valuesGroupedByCurrencies.keys()


if args['print_currency'] is None:
    args['print_currency'] = fullCurrencies
else:
    fullCurrencies = args['print_currency']

# cleanup the input array, remove duplicates
print "cleanup the input data, remove duplicates"
lastKey = ""
lastIndex = ""
for k in fullData:
    key = "#";
    for bank in fullData[k]['values']:
        for curr in fullCurrencies:
            key+= "%.6f,%.6f," % (fullData[k]['values'][bank][curr]['sell'], fullData[k]['values'][bank][curr]['buy'])
            
    if lastKey == key:
        if not args['management_hide']:
            print "    del key %s, dup of %s" % (k, lastIndex)
        del fullData[k]
    
    lastKey = key
    lastIndex = k
print ""

if args['output']=="print":
    # 20 chars: date
    # 15 chars: bank
    # EUR, USD, CHF, GBP : sale/buy : 1.4decimals : space
    # 56 =  4*2*(1+1+4+1)
    
    displaySettings = { 
        'sell':     'sell' in args['print_operation'], 
        'buy':      'buy' in args['print_operation'], 
        'days':     args['print_days'] 
    }
    
    outputFmt_currencyName = ""
    outputFmt_currencyOper = ""
    for c in fullCurrencies:
        if displaySettings['sell'] and displaySettings['buy'] :
            outputFmt_currencyName+= " % 6s%s% 7s|" % ("", c, "")
            outputFmt_currencyOper+= " % 7s| % 7s|" % ('sell', 'buy')
        elif displaySettings['sell']:
            outputFmt_currencyName+= " % 2s%s% 2s|" % ("", c, "")
            outputFmt_currencyOper+= " % 7s|" % ('sell')
        elif displaySettings['buy']:
            outputFmt_currencyName+= " % 2s%s% 2s|" % ("", c, "")
            outputFmt_currencyOper+= " % 7s|" % ('buy')
    
    outputFmt_row1 = "                    _               _"+outputFmt_currencyName
    outputFmt_row2 = "%-20s|%-15s|"+outputFmt_currencyOper

    minDateForPrint = (datetime.datetime.now() - datetime.timedelta(days=displaySettings['days'])).strftime('%Y-%m-%d 00:00:00')
    
    #print outputFmt_row1
    #print outputFmt_row2 % ("Date", "Bank")
    
    min_max = {
        'min':{
            'buy':  { },
            'sell': { },
        },
        'max':{
            'buy':  { },
            'sell': { },
        },
    }
    currencyMax = {}
    for curr in fullCurrencies:
        min_max['min']['buy'][curr] = sys.maxint/2
        min_max['min']['sell'][curr] = sys.maxint/2
        min_max['max']['buy'][curr] = -1*sys.maxint/2
        min_max['max']['sell'][curr] = -1*sys.maxint/2
    
    lk = None   # last k
    lday = None
    for k in fullData:
        day = fullData[k]['date'][0:10]
        
        if fullData[k]['date']>minDateForPrint:
            output = "%-20s|" % k
            outputBlank = "%-20s|" % ""

            if day!=lday:
                print outputFmt_row1
                print outputFmt_row2 % ("Date", "Bank")
            
            datePrinted = False
            
            #banks = collections.OrderedDict(fullData[k]['values'])
            
            # sort the banks in my custom order
            banks = collections.OrderedDict()
            bankPriority = ( 'BNR', 'CEC', 'RIB', 'AlphaBank')
            for b in bankPriority:
                if b in fullData[k]['values']:
                    banks[b] = fullData[k]['values'][b]
                    
            for b in fullData[k]['values']:
                if b not in bankPriority:
                    banks[b] = fullData[k]['values'][b]
            
            for bank in banks:
                if args['print_bank'] is None or bank in args['print_bank']:
                    if not datePrinted:
                        finalOutput = output
                    else:
                        finalOutput = outputBlank
                        
                    datePrinted = True
                    finalOutput+= "%-15s|" % bank
                    for c in fullCurrencies:
                        mark = {
                            'min': {
                                'sell': False,
                                'buy': False,
                            },
                            'max': {
                                'sell': False,
                                'buy': False,
                            },
                        }

                        if bank!='BNR':
                            value = fullData[k]['values'][bank][c]['sell']
                            if min_max['min']['sell'][c] >= value:
                                min_max['min']['sell'][c] = value
                                mark['min']['sell'] = True
                            if min_max['max']['sell'][c] <= value:
                                min_max['max']['sell'][c] = value
                                mark['max']['sell'] = True
                            
                            value = fullData[k]['values'][bank][c]['buy']
                            if min_max['min']['buy'][c] >= value:
                                min_max['min']['buy'][c] = value
                                mark['min']['buy'] = True
                            if min_max['max']['buy'][c] <= value:
                                min_max['max']['buy'][c] = value
                                mark['max']['buy'] = True
                                
                        if c in args['print_currency']:
                            if displaySettings['sell']:
                                color='white'
                                try:
                                    if lk is not None:
                                        if fullData[lk]['values'][bank][c]['sell'] > fullData[k]['values'][bank][c]['sell']:
                                            color='green'
                                        elif fullData[lk]['values'][bank][c]['sell'] < fullData[k]['values'][bank][c]['sell']:
                                            color='red'
                                except: 
                                    pass

                                value = fullData[k]['values'][bank][c]['sell']
                                
                                bgcolor = None
                                attrs = []
                                if mark['min']['sell']:
                                    attrs.append('underline')
                                    bgcolor = 'on_blue'
                                
                                
                                value_fmt = "  %s" % (colored("%1.4f" % value, color, bgcolor, attrs=attrs))
                                if args['print_diff']:
                                    if color=='white':
                                        color='grey'
                                        
                                    try:
                                        if lk is not None:
                                            value = fullData[k]['values'][bank][c]['sell'] - fullData[lk]['values'][bank][c]['sell']
                                        else:
                                            value = fullData[k]['values'][bank][c]['sell']
                                    except: 
                                        pass
                                    
                                    value_fmt = " %s" % (colored("%+0.4f" % value, color, attrs=[]))
                                    
                                finalOutput+= value_fmt
                                finalOutput+= "|"
                            if displaySettings['buy']:
                                color='white'
                                try:
                                    if lk is not None:
                                        if fullData[lk]['values'][bank][c]['buy'] > fullData[k]['values'][bank][c]['buy']:
                                            color='red'
                                        elif fullData[lk]['values'][bank][c]['buy'] < fullData[k]['values'][bank][c]['buy']:
                                            color='green'
                                except: 
                                    pass

                                value = fullData[k]['values'][bank][c]['buy']
                                value_fmt = "  %s" % (colored("%1.4f" % value, color, attrs=[]))
                                if args['print_diff']:
                                    if color=='white':
                                        color='grey'
                                    
                                    try:
                                        if lk is not None:
                                            value = fullData[k]['values'][bank][c]['buy'] - fullData[lk]['values'][bank][c]['buy']
                                        else:
                                            value = fullData[k]['values'][bank][c]['buy']
                                    except: 
                                        pass
                                    
                                    value_fmt = " %s" % (colored("%+0.4f" % value, color, attrs=[]))
                                    
                                finalOutput+= value_fmt
                                finalOutput+= "|"
                    print finalOutput
            print ""
            
        lk = k
        lday = day
    
elif args['output']=="json":
    f = open(args['file'], "w")
    f.write(json.dumps(fullData))
    f.close()

elif args['output']=="jsonp":
    f = open(args['file'], "w")
    f.write("ExchangeRateData = "+json.dumps(fullData)+";")
    f.close()
