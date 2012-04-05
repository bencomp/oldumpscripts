import json
import fileinput
import sys


if sys.argv[len(sys.argv)-1] != sys.argv[0]:
	outputfile = open(sys.argv[len(sys.argv)-1], 'wb')
else:
	sys.exit("No filename supplied!")

# Create base stats dict. countr is the record count
stats = {
	"confused": [],
	"error": []
	}


def classifications_stats(record, type):
	"""Counts classifications in the record.
	
	"""
	#if isinstance(record["classifications"], dict):
	for k in record["classifications"].keys():
		if k in stats[type]["classifications"].keys():
			stats[type]["classifications"][k] = stats[type]["classifications"][k] + 1
			if isinstance(record["classifications"][k], list):
				stats[type]["c"][k] = stats[type]["c"][k] + len(record["classifications"][k])
		else:
			stats[type]["classifications"][k] = 1
			if isinstance(record["classifications"][k], list):
				stats[type]["c"][k] = len(record["classifications"][k])
	#else:
		# classifications are not in a dict
		

def identifiers_stats(record, type):
	"""Counts identifiers in the record.
	
	"""
	for k in record["identifiers"].keys():
		if k in stats[type]["identifiers"].keys():
			stats[type]["identifiers"][k] = stats[type]["identifiers"][k] + 1
			if isinstance(record["identifiers"][k], list):
				stats[type]["i"][k] = stats[type]["i"][k] + len(record["identifiers"][k])
		else:
			stats[type]["identifiers"][k] = 1
			if isinstance(record["identifiers"][k], list):
				stats[type]["i"][k] = len(record["identifiers"][k])

def key_stats(record, type):
	"""Counts keys in the record.
	If there are identifiers and / or classifications, they are counted separately.
	"""
	for k in record.keys():
		if k in stats[type]["keys"].keys():
			stats[type]["keys"][k] = stats[type]["keys"][k] + 1
		else:
			stats[type]["keys"][k] = 1
	
	if "identifiers" in record.keys():
		identifiers_stats(record, type)
	if "classifications" in record.keys():
		classifications_stats(record, type)

def determine_type(object):
	if object["key"][0:8] == "/authors":
		if object["type"]["key"] == "/type/author":
			return "author"
		elif object["type"]["key"] == "/type/redirect":
			return "redirect_author"
		elif object["type"]["key"] == "/type/delete":
			return "deleted_author"
		else:
			stats["confused"].append((object["type"]["key"],object["key"]))
			return "confused_author"
	elif object["key"][0:6] == "/books":
		if object["type"]["key"] == "/type/edition":
			return "edition"
		elif object["type"]["key"] == "/type/redirect":
			return "redirect_edition"
		elif object["type"]["key"] == "/type/delete":
			return "deleted_edition"
		else:
			stats["confused"].append((object["type"]["key"],object["key"]))
			return "confused_edition"
	elif object["key"][0:6] == "/works":
		if object["type"]["key"] == "/type/work":
			return "work"
		elif object["type"]["key"] == "/type/redirect":
			return "redirect_work"
		elif object["type"]["key"] == "/type/delete":
			return "deleted_work"
		else:
			stats["confused"].append((object["type"]["key"],object["key"]))
			return "confused_work"
	elif object["type"]["key"] == "/type/redirect":
		return "redirect"
	elif object["type"]["key"] == "/type/delete":
		return "delete"
	elif object["type"]["key"] == "/type/subject":
		return "subject"
	elif object["type"]["key"] == "/type/page":
		return "page"
	elif object["type"]["key"] == "/type/template":
		return "template"
	elif object["type"]["key"] == "/type/i18n":
		return "i18n"
	elif object["type"]["key"] == "/type/language":
		return "language"
	elif object["type"]["key"] == "/type/type":
		return "type"
	elif object["type"]["key"] == "/type/property":
		return "property"
	elif object["type"]["key"] == "/type/library":
		return "library"
	elif object["type"]["key"] == "/type/macro":
		return "macro"
	elif object["type"]["key"] == "/type/rawtext":
		return "rawtext"
	elif object["type"]["key"] == "/type/home":
		return "home"
	elif object["type"]["key"] == "/type/usergroup":
		return "usergroup"
	elif object["type"]["key"] == "/type/i18n_page":
		return "i18n_page"
	else:
		stats["confused"].append((object["type"]["key"],object["key"]))
		return "confused"

# Open standard input
f = fileinput.input('-')
for line in f:
	record = json.loads(line)
	
	# determine record type
	t = determine_type(record)
	if t == "confused":
		continue
	
	# do stuff
	if t in stats.keys():
		stats[t]["countr"] = stats[t]["countr"] + 1
	else:
		stats[t] = {"countr": 1, "keys": {}, "classifications": {}, "c": {}, "identifiers": {}, "i": {}}
		print "new type:", t
	
	try:
		key_stats(record, t)
	except Exception as e:
		stats["error"].append((record, str(e)))

json.dump(stats, outputfile, indent=2)