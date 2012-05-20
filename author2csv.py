import json
import fileinput
import csv
import sys
import codecs

# Creates a CSV file from Author records in an Open Library dump file.

# Usage: sed -nrf author2-json.txt <ol_dump> | python author2csv.py authors.csv
# where author2-json.txt makes sed output the JSON documents, but only for author-type records.

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    fn = sys.argv[len(sys.argv)-1]
    writer = csv.writer(open(fn, 'wb'))
    writer.writerow(["Author key","Name","Slug","Date of birth","DoB slug","Date of Death","DoD slug"])
    writer2 = csv.writer(open("noname-"+fn, 'wb'))
else:
    sys.exit("No filename supplied!")

def createSlug(input):
    slug = unicode(input).lower() # .strip('. /,:;-_\\!@#$%^&*()+=\'".\sʻ')
    slug = slug.replace('.','')
    slug = slug.replace(' ','')
    slug = slug.replace(',','')
    slug = slug.replace(':','')
    slug = slug.replace(';','')
    slug = slug.replace('-','')
    slug = slug.replace('\'','')
    slug = slug.replace('"','')
    slug = slug.replace('(','')
    slug = slug.replace(')','')
    slug = slug.replace('&','')
    slug = slug.replace('_','')
    return slug

# Open standard input
f = fileinput.input('-')
for line in f:
    record = json.loads(line)
    if "name" in record.keys():
        slug = createSlug(record["name"])
        
        dob, dobslug = None, None
        if "birth_date" in record.keys() and record["birth_date"] != "":
            dob = record["birth_date"]
            dobslug = createSlug(dob)
            
        dod, dodslug = None, None
        if "death_date" in record.keys() and record["death_date"] != "":
            dod = record["death_date"]
            dodslug = createSlug(dod)
            
        
        writer.writerow([unicode(record["key"]).replace('/authors/','').encode('utf-8'), unicode(record["name"]).encode('utf-8'), unicode(slug).encode('utf-8'), unicode(dob).encode('utf-8'), unicode(dobslug).encode('utf-8'), unicode(dod).encode('utf-8'), unicode(dodslug).encode('utf-8')])
    else:
        writer2.writerow([unicode(record["key"]).replace('/authors/','').encode('utf-8')])
