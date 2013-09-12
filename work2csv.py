import json
import fileinput
import csv
import sys
import codecs

# Creates a CSV file from Work records in an Open Library dump file.

# Usage: sed -nrf work2-json.txt <ol_dump> | python work2csv.py works.csv
# where work2-json.txt makes sed output the JSON documents, but only for work-type records.

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    fn = sys.argv[len(sys.argv)-1]
    writer = csv.writer(open(fn, 'wb'))
    writer.writerow(["Work key","Title","Slug","Subtitle","Subtitle slug","Number of authors","First author"])
    errorrecords = open(fn+"-error.txt", 'wb')
else:
    sys.exit("No filename supplied!")

def createSlug(input):
    slugg = unicode(input).lower() # .strip('. /,:;-_\\!@#$%^&*()+=\'".\sʻ')
    slugg = slugg.replace('.','')
    slugg = slugg.replace(' ','')
    slugg = slugg.replace(',','')
    slugg = slugg.replace(':','')
    slugg = slugg.replace(';','')
    slugg = slugg.replace('-','')
    slugg = slugg.replace('\'','')
    slugg = slugg.replace('"','')
    slugg = slugg.replace('(','')
    slugg = slugg.replace(')','')
    slugg = slugg.replace('&','')
    slugg = slugg.replace('_','')
    return slugg
    
# Open standard input
f = fileinput.input('-')
title_max_length = 0
subtitle_max_length = 0

for line in f:
    record = json.loads(line)
    
    title, slug = None, None
    if "title" in record.keys():
        title = record["title"]
        title_max_length = max(len(title), title_max_length)
        slug = createSlug(title)
        
    sub, subslug = None, None
    if "subtitle" in record.keys():
        sub = record["subtitle"]
        subtitle_max_length = max(len(sub), subtitle_max_length)
        subslug = createSlug(sub)
            
    num_authors, first_author = None, None
    if "authors" in record.keys() and len(record["authors"]) != 0:
        num_authors = len(record["authors"])
        if "author" in record["authors"][0].keys():
            first_author = record["authors"][0]["author"]["key"].replace('/authors/','')
        else:
            # write issue to error file
            errorrecords.write(record["key"] + "\tAuthor field found, but no author.\n")
            num_authors = -num_authors
            
    writer.writerow([unicode(record["key"]).replace('/works/','').encode('utf-8'), unicode(title).encode('utf-8'), unicode(slug).encode('utf-8'), unicode(sub).encode('utf-8'), unicode(subslug).encode('utf-8'), num_authors, unicode(first_author).encode('utf-8')])

print "title_max_length:", title_max_length
print "subtitle_max_length:", subtitle_max_length