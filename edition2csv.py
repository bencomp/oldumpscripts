import json
import fileinput
import csv
import sys
import codecs, cStringIO

# Creates a CSV file from Edition records in an Open Library dump file.

# Usage: sed -nrf edition2-json.txt <ol_dump> | python edition2csv.py editions.csv
# where edition2-json.txt makes sed output the JSON documents, but only for edition-type records.

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([(s if isinstance(s, int) else s.encode("utf-8"))  for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    fn = sys.argv[len(sys.argv)-1]
    writer = UnicodeWriter(open(fn, 'wb'))
    writer.writerow(["Edition key","Title","Slug","Subtitle","Subtitle slug","Number of works","First work","Number of authors","First author","Number of publishers","First publisher","Publisher slug","Number of publish places","First publish place","Publish place slug","Publication year", "Format", "Dimensions", "Weight", "Number of pages"])
    errorrecords = open(fn+"-error.txt", 'wb')
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
title_max_length = 0
subtitle_max_length = 0
publisher_max_length = 0
publishplace_max_length = 0
pubdate_max_length = 0
key_max_length = 0
format_max_length = 0
dimensions_max_length = 0
weight_max_length = 0

for line in f:
    record = json.loads(line)
    
    key = record["key"].replace('/books/','')
    key_max_length = max(len(key), key_max_length)
    
    title, slug = "", ""
    if "title" in record.keys():
        title = record["title"]
        title_max_length = max(len(title), title_max_length)
        slug = createSlug(title)
        
    sub, subslug = "", ""
    if "subtitle" in record.keys():
        sub = record["subtitle"]
        subtitle_max_length = max(len(sub), subtitle_max_length)
        subslug = createSlug(sub)
            
    num_works, first_work = 0, ""
    if "works" in record.keys() and len(record["works"]) != 0:
        num_works = len(record["works"])
        if "key" in record["works"][0].keys():
            first_work = record["works"][0]["key"].replace('/works/','')
        else:
            # write issue to error file
            errorrecords.write(record["key"] + "\tWork field found, but no work.\n")
            num_works = -num_works
            
    num_authors, first_author = "", ""
    if "authors" in record.keys() and len(record["authors"]) != 0:
        num_authors = len(record["authors"])
        if isinstance(record["authors"][0], dict):
            if "key" in record["authors"][0].keys():
                first_author = record["authors"][0]["key"].replace('/authors/','')
            else:
                # write issue to error file
                errorrecords.write(record["key"] + "\tAuthor field found, but no author.\n")
                num_authors = -num_authors
        else:
            errorrecords.write(record["key"] + "\tAuthor field found, but first author is not a dict.\n")
    
    num_publishers, first_publisher, publisherslug = 0, "", ""
    if "publishers" in record.keys() and len(record["publishers"]) != 0:
        num_publishers = len(record["publishers"])
        first_publisher = record["publishers"][0]
        publisher_slug = createSlug(first_publisher)
        publisher_max_length = max(len(first_publisher), publisher_max_length)
    elif "publishers" in record.keys() and len(record["publishers"]) == 0:
        # write issue to error file
        errorrecords.write(record["key"] + "\tPublisher field found, but no publisher. (empty list)\n")
    
    num_publishplaces, first_publishplace, publishplaceslug = 0, "", ""
    if "publish_places" in record.keys() and len(record["publish_places"]) != 0:
        num_publishplaces = len(record["publish_places"])
        first_publishplace = record["publish_places"][0]
        publishplaceslug = createSlug(first_publishplace)
        publishplace_max_length = max(len(first_publishplace), publishplace_max_length)
    
    pubdate = ""
    if "publish_date" in record.keys():
        pubdate = record["publish_date"]
        pubdate_max_length = max(len(pubdate), pubdate_max_length)
        
    format = ""
    if "physical_format" in record.keys():
        format = record["physical_format"]
        format_max_length = max(len(format), format_max_length)
    
    dimensions = ""
    if "physical_dimensions" in record.keys():
        dimensions = record["physical_dimensions"]
        dimensions_max_length = max(len(dimensions), dimensions_max_length)
    
    weight = ""
    if "weight" in record.keys():
        weight = record["weight"]
        weight_max_length = max(len(weight), weight_max_length)
    
    number_of_pages = 0
    if "number_of_pages" in record.keys():
        number_of_pages = record["number_of_pages"]
    
    writer.writerow([key, title, slug, sub, subslug, num_works, first_work, num_authors, first_author, num_publishers, first_publisher, publisher_slug, num_publishplaces, first_publishplace, publishplaceslug, pubdate, format, dimensions, weight, number_of_pages])

print "title_max_length:", title_max_length
print "subtitle_max_length:", subtitle_max_length
print "publisher_max_length:", publisher_max_length
print "publishplace_max_length:", publishplace_max_length
print "pubdate_max_length:", pubdate_max_length
print "key_max_length:", key_max_length
print "format_max_length:", format_max_length
print "dimensions_max_length:", dimensions_max_length