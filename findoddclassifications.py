import json
import fileinput
import csv
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	writer = csv.writer(open(sys.argv[len(sys.argv)-1], 'wb'))
	writer.writerow(["record","classification","value"])
else:
	sys.exit("No filename supplied!")

oddids = ["lccn_permalink", 
	"depósito_legal_n.a.",  
	"udc", 
	"identificativo_sbn",
	"finnish_public_libraries_classification_system",
	"rvk",
	"library_and_archives_canada_cataloguing_in_publication",
	"goethe_university_library,_frankfurt", 
	"lccn_permalink:_http:/lccn.loc.gov/65023044", 
	"siso", 
	"entertaining_tvshows_online",
	"national_library_of_canada_catologue",
	"nlm_class_no.:", 
	"ulrls_classmark"]

# Open standard input
f = fileinput.input('-')
for line in f:
	decoded = json.loads(line)
	if "classifications" in decoded:
		if isinstance(decoded["classifications"], dict):
			for k in decoded["classifications"].keys():
				if k.encode('utf-8') in oddids:
					for v in decoded["classifications"][k]:
						writer.writerow([decoded["key"].encode('utf-8'), k.encode('utf-8'), v.encode('utf-8')])

