import json
import fileinput
import csv
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	writer = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
	writer.writerow(["record","identifier","value"])
else:
	sys.exit("No filename supplied!")

oddids = ["genres","notes","original_languages","other_titles","table_of_contents","translated_titles"]

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
				writer.writerow([decoded["key"].encode('utf-8'), k.encode('utf-8'), decoded[k].encode('utf-8')])

