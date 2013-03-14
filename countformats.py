import json
import fileinput
import sys

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    file = open(sys.argv[len(sys.argv)-1], 'w')
    file.write("format\t\"total occurrences\"\n")
else:
    sys.exit("No filename supplied!")

countr = {}
nrformats = 0

# Open standard input
f = fileinput.input('-')
for line in f:
    decoded = json.loads(line)
    if "physical_format" in decoded:
        k = decoded["physical_format"]
        if k in countr.keys():
            countr[k] = countr[k] + 1
        else:
            countr[k] = 1
            nrformats = nrformats + 1
            print "new format ("+ str(nrformats) +"):", k.encode('utf-8')

keys = countr.keys()
keys.sort()
for k in keys:
    file.write(k.encode('utf-8') + "\t{0}\n".format(countr[k]))