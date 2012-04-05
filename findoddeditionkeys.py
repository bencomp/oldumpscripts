import json
import fileinput
import csv
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	writer = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
	writer.writerow(["record","identifier","value"])
else:
	sys.exit("No filename supplied!")

oddids = ["coverid","displayname","edition","ia_id","macro","news","price",
	"stats","volume_number","website","code","dewry_decimal_class",
	"library_of_congress_name","birth_date","body","dimensions",
	"lc_classification","by_statements","name","bookweight","language_code",
	"volumes","isbn","create","isbn_odd_length","isbn_invalid","links","url"]

# Open standard input
f = fileinput.input('-')
for line in f:
	decoded = json.loads(line)
	for k in decoded.keys():
		if k in oddids:
			if isinstance(decoded[k], list) or isinstance(decoded[k], dict):
				for v in decoded[k]:
					writer.writerow([decoded["key"].encode('utf-8'), k.encode('utf-8'), unicode(v).encode('utf-8')])
			else:
				writer.writerow([decoded["key"].encode('utf-8'), k.encode('utf-8'), unicode(decoded[k]).encode('utf-8')])

