import json
import csv
import sys

def export_csv(stats, basename):
  for type in stats.keys():
    if type not in ["error", "confused"]:
      outfile = basename+"-"+type+".csv"
      file = open(outfile, 'wb')
      writer = csv.writer(file)
      writer.writerow(["key".encode('utf-8'), "number".encode('utf-8')])
      writer.writerow(["total records".encode('utf-8'), stats[type]["countr"]])
      for k in stats[type]["keys"].keys():
        writer.writerow([k.encode('utf-8'), stats[type]["keys"][k]])
      if len(stats[type]["identifiers"]) > 0:
        idfile = basename+"-"+type+"-ids.csv"
        writer = csv.writer(open(idfile, 'wb'))
        writer.writerow(["identifier".encode('utf-8'), "number of records".encode('utf-8'), 
          "number of instances".encode('utf-8')])
        for id in stats[type]["identifiers"].keys():
          writer.writerow([id.encode('utf-8'), stats[type]["identifiers"][id], 
            stats[type]["i"][id]])
      if len(stats[type]["classifications"]) > 0:
        clfile = basename+"-"+type+"-cls.csv"
        writer = csv.writer(open(clfile, 'wb'))
        writer.writerow(["classification".encode('utf-8'), "number of records", 
          "number of instances"])
        for id in stats[type]["classifications"].keys():
          writer.writerow([unicode(id).encode('utf-8'), stats[type]["classifications"][id], 
            stats[type]["c"][id]])
      print outfile, "written."


def load():
  if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    statsfile = open(sys.argv[len(sys.argv)-1], 'rb')
    stats = json.load(statsfile)
    export_csv(stats, sys.argv[len(sys.argv)-1])
  else:
    sys.exit("No filename supplied!")

if __name__ == "__main__":
  load()
