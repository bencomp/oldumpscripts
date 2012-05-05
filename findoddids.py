import json
import fileinput
import csv
import sys

# Usage: sed -nrf edition-json.txt <ol_dump> | python oddids.txt oddids.csv
# where edition-json.txt makes sed output the JSON documents, but only for edition-type records.

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    writer = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
    writer.writerow(["record","identifier","value"])
else:
    sys.exit("No filename supplied!")

idfile = open(sys.argv[1], 'rU')
oddids = []
for l in idfile:
    print l.strip()
    oddids.append(l.strip())

# Open standard input
f = fileinput.input('-')
for line in f:
    decoded = json.loads(line)
    if "identifiers" in decoded:
        for k in decoded["identifiers"].keys():
            if k.encode('utf-8') in oddids:
                for v in decoded["identifiers"][k]:
                    writer.writerow([decoded["key"].encode('utf-8'), k.encode('utf-8'), v.encode('utf-8')])

