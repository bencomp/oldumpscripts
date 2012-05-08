import json
import fileinput
import sys
import codecs

"""Creates a JSON file with statistics.

Usage: sed -nre "s/^[^{]*//p" <ol_dump_file> | python stats.py output.json

This script reads the standard input, one JSON record from Open Library per line,
and basically counts keys, classifications and identifiers. Keys are counted for 
separate record types (author, edition, work, etc.); classifications and identifiers are 
counted when available.

"""
if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    outputfile = codecs.open(sys.argv[len(sys.argv)-1], 'wb','utf-8')
else:
    sys.exit("No filename supplied!")

# Create base stats dict. countr is the record count
stats = {
    "confused": [],
    "error": []
    }

# special keys: classifications and identifiers that are lists (hence no ocaid),
# outside the classifications and identifiers objects.
special_class = ["lc_classifications", "dewey_decimal_class"]
special_id    = ["isbn_10", "isbn_13", "lccn", "oclc_numbers"]

def classifications_stats(record, type):
    """Counts classifications in the record.
    
    """
    """for c in special_class:
        if c in record.keys():
            stats[type]["sc"][c][0] = stats[type]["sc"][c][0] + 1
            stats[type]["sc"][c][1] = stats[type]["sc"][c][1] + len(record[c])
            if len(record[c]) == 0:
                stats[type]["sc"][c][2] = stats[type]["sc"][c][2] + 1
    """
    for k in record["classifications"].keys():
        if k in stats[type]["classifications"].keys():
            stats[type]["classifications"][k][0] = stats[type]["classifications"][k][0] + 1
            if isinstance(record["classifications"][k], list):
                stats[type]["classifications"][k][1] = stats[type]["classifications"][k][1] + len(record["classifications"][k])
                if len(record["classifications"][k]) == 0: # empty list
                    stats[type]["classifications"][k][2] = stats[type]["classifications"][k][2] + 1
            else:
                stats[type]["classifications"][k][1] = stats[type]["classifications"][k][1] + 1
        else:
            stats[type]["classifications"][k] = [1,1,0]
            if isinstance(record["classifications"][k], list):
                stats[type]["classifications"][k][1] = len(record["classifications"][k])
                if len(record["classifications"][k]) == 0: # empty list
                    stats[type]["classifications"][k][2] = stats[type]["classifications"][k][2] + 1
                
        

def identifiers_stats(record, type):
    """Counts identifiers in the record.
    
    """
    # 'top-level' identifiers
    """for i in special_id:
        if i in record.keys():
            stats[type]["si"][i][0] = stats[type]["si"][i][0] + 1
            stats[type]["si"][i][1] = stats[type]["si"][i][1] + len(record[i])
            if len(record[i]) == 0:
                stats[type]["si"][i][2] = stats[type]["si"][i][2] + 1
    """
    # 'normal' identifiers
    for k in record["identifiers"].keys():
        if k in stats[type]["identifiers"].keys():
            stats[type]["identifiers"][k][0] = stats[type]["identifiers"][k][0] + 1
            if isinstance(record["identifiers"][k], list):
                stats[type]["identifiers"][k][1] = stats[type]["identifiers"][k][1] + len(record["identifiers"][k])
                if len(record["identifiers"][k]) == 0: # empty list
                    stats[type]["identifiers"][k][2] = stats[type]["identifiers"][k][2] + 1
            else:
                stats[type]["identifiers"][k][1] = stats[type]["identifiers"][k][1] + 1
        else:
            stats[type]["identifiers"][k] = [1,1,0]
            if isinstance(record["identifiers"][k], list):
                stats[type]["identifiers"][k][1] = len(record["identifiers"][k])
                if len(record["identifiers"][k]) == 0: # empty list
                    stats[type]["identifiers"][k][2] = stats[type]["identifiers"][k][2] + 1

def key_stats(record, type):
    """Counts keys in the record.
    If there are identifiers and / or classifications, they are counted separately.
    """
    for k in record.keys():
        if k in stats[type]["keys"].keys():
            stats[type]["keys"][k][0] = stats[type]["keys"][k][0] + 1
            if isinstance(record[k], list):
                stats[type]["keys"][k][1] = stats[type]["keys"][k][1] + len(record[k])
                if len(record[k]) == 0: # empty list
                    stats[type]["keys"][k][2] = stats[type]["keys"][k][2] + 1
            else:
                stats[type]["keys"][k][1] = stats[type]["keys"][k][1] + 1
        else:
            stats[type]["keys"][k] = [1,1,0]
            if isinstance(record[k], list):
                stats[type]["keys"][k][1] = len(record[k])
                if len(record[k]) == 0: # empty list
                    stats[type]["keys"][k][2] = stats[type]["keys"][k][2] + 1
    
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
        elif object["type"]["key"] == "/type/volume":
            return "volume"
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
        stats[t] = {"countr": 1, "keys": {}, "classifications": {}, "sc": {}, "identifiers": {}, "si": {}}
        #for c in special_class:
        #    stats[t]["sc"][c] = [0,0,0]
        #for i in special_id:
        #    stats[t]["si"][i] = [0,0,0]
        print "new type:", t
    
    try:
        key_stats(record, t)
    except Exception as e:
        print record["key"], sys.exc_info()
        stats["error"].append((record, str(e)))

json.dump(stats, outputfile, indent=2)