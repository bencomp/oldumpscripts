import json
import fileinput
import sys

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	file = open(sys.argv[len(sys.argv)-1], 'w')
	file.write("classification,\"total occurrences\",\"record occurrences\"\n")
else:
	sys.exit("No filename supplied!")

ids = ["lc_classifications", "dewey_decimal_class"]
count,countr = {},{}

for i in ids:
	count[i] = 0
	countr[i] = 0

# Open standard input
f = fileinput.input('-')
for line in f:
	decoded = json.loads(line)
	for a in ids:
		if a in decoded:
			count[a] = count[a] + len(decoded[a]) # works b/c decoded[a] is a sequence
			countr[a] = countr[a] + 1
	if "classifications" in decoded:
		if isinstance(decoded["classifications"], dict):
			for k in decoded["classifications"].keys():
				if k in count.keys():
					count[k] = count[k] + len(decoded["classifications"][k])
					countr[k] = countr[k] + 1
				else:
					count[k] = len(decoded["classifications"][k])
					countr[k] = 1
		else:
			print decoded["key"] + "," + unicode(decoded["classifications"])

keys = count.keys()
keys.sort()
for k in keys:
	file.write(k.encode('utf-8') + ",{0},{1}\n".format(count[k], countr[k]))