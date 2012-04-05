import json
import fileinput
import sys
import csv

# Exports the given LCC and DDC classifications for input in DBMS.

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	file = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
else:
	sys.exit("No filename supplied!")

ids = ["lc_classifications", "dewey_decimal_class"]
n = 0

f = open(sys.argv[1], 'r')
for line in f:
	record = json.loads(line[line.index('{'):])
	if record["key"][0:6] == "/books" and record["type"]["key"] == "/type/edition":
		n = n + 1
		if n % 100000 == 0:
			print n, "records processed,"
		#for a in ids:
		if "lc_classifications" in record.keys():
			for c in record["lc_classifications"]:
				file.writerow([record["key"],"lcc",c.encode('utf-8')])
		if "dewey_decimal_class" in record.keys():
			for c in record["dewey_decimal_class"]:
				file.writerow([record["key"],"ddc",c.encode('utf-8')])
	
