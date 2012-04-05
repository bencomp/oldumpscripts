import json
import fileinput
import csv
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	writer = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
	writer.writerow(["record","identifier","value"])
else:
	sys.exit("No filename supplied!")

oddids = ["     _date","authors","body","by_statement","contributions","covers","create","description","dewey_decimal_class",
	"edition_name","entity_type","first_sentence","genres","identifiers","isbn_10","isbn_13","languages","lc_classifications",
	"lccn","marc","notes","number_of_pages","numeration","ocaid","oclc_numbers","other_titles","pagination","physical_format",
	"publish_country","publish_date","publish_places","publishers","role","series","source_records","subject_place",
	"subject_time","subjects","subtitle","table_of_contents","tags","title_prefix","website_name","works"]

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

