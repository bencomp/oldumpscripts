import json
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	file = open(sys.argv[len(sys.argv)-1], 'rb')
	errorfile = open(sys.argv[len(sys.argv)-1]+"errors.txt", 'wb')
else:
	sys.exit("No filename supplied!")

stats = json.load(file)
for r in stats["error"]:
	errorfile.write(r[0]["key"]+","+str(r[1])+"\n")