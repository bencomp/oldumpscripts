import json
import fileinput
import sys

# Counts the given LCC and DDC classifications. Worst case: every classification unique...

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	file = open(sys.argv[len(sys.argv)-1], 'w')
else:
	sys.exit("No filename supplied!")

ids = ["lc_classifications", "dewey_decimal_class"]
count = {}
n = 0

for i in ids:
	count[i] = {}

f = open(sys.argv[1], 'r')
for line in f:
	record = json.loads(line[line.index('{'):])
	if record["key"][0:6] == "/books" and record["type"]["key"] == "/type/edition":
		n = n + 1
		if n % 100000 == 0:
			print n, "records processed,", len(count["lc_classifications"].keys()),  len(count["dewey_decimal_class"].keys())
		#for a in ids:
		if "lc_classifications" in record.keys():
			for c in record["lc_classifications"]:
				if c in count["lc_classifications"].keys():
					count["lc_classifications"][c] = count["lc_classifications"][c] + 1
				else:
					count["lc_classifications"][c] = 1
		if "dewey_decimal_class" in record.keys():
			for c in record["dewey_decimal_class"]:
				if c in count["dewey_decimal_class"].keys():
					count["dewey_decimal_class"][c] = count["dewey_decimal_class"][c] + 1
				else:
					count["dewey_decimal_class"][c] = 1
	
json.dump(count, file, indent=2, sort_keys=True)