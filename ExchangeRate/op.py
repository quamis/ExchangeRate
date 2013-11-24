#!/usr/bin/python
import os, re, json
import collections
import argparse
import datetime
from termcolor import colored, cprint

parser = argparse.ArgumentParser(description='Make an internal money operation. Ex: op.py buy 100 EUR 4.44')
parser.add_argument('operation', 	action='store', type=str,   default="print", help='TODO')
parser.add_argument('amount', 		action='store', type=float, default=0,    help='TODO')
parser.add_argument('currency', 	action='store', type=str,   default='???',help='TODO')
parser.add_argument('exchangeRate', action='store', type=float, default=0,    help='TODO')

#parser.add_argument('--test-args',		dest='test_args',		action='store', type=str,  default=None,help='TODO')
args = vars(parser.parse_args())
FILE_HIST = "op/history.json"
FILE_BANK = "op/bank.json"

try:
	history = json.load(open(FILE_HIST))
except:
	print "Cannot open history, assuuming empty file"
	history = []
		
if args['operation']== 'buy' or args['operation']=='sell':
	json_data = {}
	json_data['date'] = 			datetime.datetime.now().isoformat(' ')
	json_data['operation'] =		args['operation']
	json_data['amount'] = 			args['amount']
	json_data['currency'] = 		args['currency']
	json_data['exchangeRate'] = 	args['exchangeRate']

	# write into the history file
	history.append(json_data)

	f = open(FILE_HIST, "wt")
	f.write(json.dumps(history))
	f.close()


bank = { }
for op in history:
	if op['currency'] not in bank:
		bank[op['currency']] = 0
	
	op['amount'] = (-1*op['amount'] if op['operation']=='sell' else op['amount'])
	
	bank[op['currency']]+= op['amount']

print "Current bank status:"
for currency in bank:
	print "    %s: %.2f" % (currency, bank[currency])
print ""

	
