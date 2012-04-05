import json
import fileinput
import csv
import sys

countr = {}
if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	writer = csv.DictWriter(open(sys.argv[len(sys.argv)-1], 'wb'),["key","record occurrences"])

# Open standard input
f = fileinput.input('-')
for line in f:
	decoded = json.loads(line)
	for k in decoded:
		if k in countr.keys():
			countr[k] = countr[k] + 1
		else:
			countr[k] = 1

keys = countr.keys()
keys.sort()

for k in keys:
	writer.writerow({"key": k, "record occurrences": countr[k]})
	print k + ": {0}".format(countr[k])