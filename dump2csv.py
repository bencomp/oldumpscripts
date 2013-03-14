import simplejson
import fileinput
import csv
import sys
import codecs,cStringIO

# Creates CSV files from an Open Library dump file.

# <fnp>-works.csv
# <fnp>-authors.csv
# <fnp>-editions.csv
# <fnp>-works_authors.csv
# <fnp>-editions_authors.csv
# <fnp>-editions_works.csv
# <fnp>-editions_languages.csv

# Usage: sed -nre "s/^[^{]*//p" <ol_dump> | python dump2csv.py <file name prefix>

if sys.argv[len(sys.argv)-1] != sys.argv[0]:
    fnp = sys.argv[len(sys.argv)-1]
    of_works                = csv.writer(open(fnp+"-works.csv", 'wb'))
    of_authors              = csv.writer(open(fnp+"-authors.csv", 'wb'))
    of_editions             = csv.writer(open(fnp+"-editions.csv", 'wb'))
    of_works_authors        = csv.writer(open(fnp+"-works_authors.csv", 'wb'))
    of_editions_authors     = csv.writer(open(fnp+"-editions_authors.csv", 'wb'))
    of_editions_works       = csv.writer(open(fnp+"-editions_works.csv", 'wb'))
    of_editions_languages   = csv.writer(open(fnp+"-editions_languages.csv", 'wb'))
    of_editions_publishers  = csv.writer(open(fnp+"-editions_publishers.csv", 'wb'))
    
    of_errors               = csv.writer(open(fnp+"-errors.csv", 'wb'))
    of_maxlengths           = open(fnp+"-maxlengths.json", 'wb')
else:
    sys.exit("No filename prefix supplied!")

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
    
def determine_type(object):
    if object["key"][0:8] == "/authors":
        if object["type"]["key"] == "/type/author":
            return "author"
    elif object["key"][0:6] == "/books":
        if object["type"]["key"] == "/type/edition":
            return "edition"
        elif object["type"]["key"] == "/type/volume":
            return "volume"
    elif object["key"][0:6] == "/works":
        if object["type"]["key"] == "/type/work":
            return "work"
    elif object["type"]["key"] == "/type/subject":
        return "subject"
    elif object["type"]["key"] == "/type/language":
        return "language"
    else:
        return "other"
    
def handle_error(row):
    enc(of_errors,row)
    print row

def enc(file, row):
    row2 = []
    for v in row:
        if isinstance(v, unicode):
            row2.append(v.encode("utf-8"))
        else:
            row2.append(v)
    
    file.writerow(row2)
    
# Open standard input
f = fileinput.input('-')

ml = {"work": {"title": 0, "titleslug": 0, "subtitle": 0, "subtitleslug": 0},
    "edition": {"title": 0, "titleslug": 0, "subtitle": 0, "subtitleslug": 0, "publisher": 0, "publisherslug": 0, "pubdate": 0},
    "author": {"name": 0, "nameslug": 0, "dob": 0, "dobslug": 0, "dod": 0, "dodslug": 0},
    "key": 0}

numrecords = 0


for line in f:
    record = simplejson.loads(line.strip())
    
    # determine record type
    t = determine_type(record)
    if t == "other":
        continue
    
    # EDITIONS
    if t == "edition":
        key = record["key"].replace('/books/','')
        
        
        title, slug = None, None
        if "title" in record.keys():
            title = record["title"]
            ml[t]["title"] = max(len(title), ml[t]["title"])
            slug = createSlug(title)
            ml[t]["titleslug"] = max(len(slug), ml[t]["titleslug"])
            
        sub, subslug = None, None
        if "subtitle" in record.keys():
            sub = record["subtitle"]
            ml[t]["subtitle"] = max(len(sub), ml[t]["subtitle"])
            subslug = createSlug(sub)
            ml[t]["subtitleslug"] = max(len(subslug), ml[t]["subtitleslug"])
                
        num_works, first_work = None, None
        if "works" in record.keys() and len(record["works"]) != 0:
            num_works = len(record["works"])
            try:
                first_work = record["works"][0]["key"].replace('/works/','')
                for work in record["works"]:
                    enc(of_editions_works,[key, work["key"].replace('/works/','')])
            except Exception as e:
                handle_error([key, "work", str(e)])
                num_works = -num_works
                
        num_authors, first_author = None, None
        if "authors" in record.keys() and len(record["authors"]) != 0:
            num_authors = len(record["authors"])
            try:
                first_author = record["authors"][0]["key"].replace('/authors/','')
                for author in record["authors"]:
                    enc(of_editions_authors,[key, author["key"].replace('/authors/','')])
            except Exception as e:
                handle_error([key, "author", str(e)])
                num_authors = -num_authors
            
        
        num_publishers, first_publisher, publisherslug = None, None, None
        if "publishers" in record.keys():
            num_publishers = len(record["publishers"])
            try:
                first_publisher = record["publishers"][0]
                publisher_slug = createSlug(first_publisher)
                for pub in record["publishers"]:
                    ml[t]["publisher"] = max(len(pub), ml[t]["publisher"])
                    pubslug = createSlug(pub)
                    ml[t]["publisherslug"] = max(len(pubslug), ml[t]["publisherslug"])
                    enc(of_editions_publishers,[key, pub, pubslug])
            except Exception as e:
                handle_error([key, "publisher", str(e)])
        
        if "languages" in record.keys():
            try:
                for lang in record["languages"]:
                    enc(of_editions_languages,[key, lang["key"].replace("/languages/", "")])
            except Exception as e:
                handle_error([key, "language", str(e)])
        
        pubdate = None
        if "publish_date" in record.keys():
            pubdate = record["publish_date"]
            ml[t]["pubdate"] = max(len(pubdate), ml[t]["pubdate"])
        
        enc(of_editions,[key, title, slug, sub, subslug, num_works, first_work, num_authors, first_author, num_publishers, first_publisher, publisher_slug, pubdate])
    
    # WORKS
    if t == "work":
        key = record["key"].replace('/works/','')
        
        title, slug = None, None
        if "title" in record.keys():
            title = record["title"]
            ml[t]["title"] = max(len(title), ml[t]["title"])
            slug = createSlug(title)
            ml[t]["titleslug"] = max(len(slug), ml[t]["titleslug"])
            
        sub, subslug = None, None
        if "subtitle" in record.keys():
            sub = record["subtitle"]
            ml[t]["subtitle"] = max(len(sub), ml[t]["subtitle"])
            subslug = createSlug(sub)
            ml[t]["subtitleslug"] = max(len(subslug), ml[t]["subtitleslug"])
                
        num_authors, first_author = None, None
        if "authors" in record.keys() and len(record["authors"]) != 0:
            num_authors = len(record["authors"])
            try:
                first_author = record["authors"][0]["author"]["key"].replace('/authors/','')
                for author in record["authors"]:
                    enc(of_works_authors,[key, author["author"]["key"].replace('/authors/','')])
            except Exception as e:
                handle_error([key, "author", str(e)])
                num_authors = -num_authors
                
        enc(of_works,[key, title, slug, sub, subslug, num_authors, first_author])
    
    # AUTHORS
    if t == "author":
        key = record["key"].replace('/authors/','')
        
        try:
            slug = createSlug(record["name"])
            ml[t]["name"] = max(len(record["name"]), ml[t]["name"])
            ml[t]["slug"] = max(len(slug), ml[t]["slug"])
            
            dob, dobslug = None, None
            if "birth_date" in record.keys() and record["birth_date"] != "":
                dob = record["birth_date"]
                dobslug = createSlug(dob)
                ml[t]["dob"] = max(len(dob), ml[t]["dob"])
                ml[t]["dobslug"] = max(len(dobslug), ml[t]["dobslug"])
                
            dod, dodslug = None, None
            if "death_date" in record.keys() and record["death_date"] != "":
                dod = record["death_date"]
                dodslug = createSlug(dod)
                ml[t]["dod"] = max(len(dod), ml[t]["dod"])
                ml[t]["dodslug"] = max(len(dodslug), ml[t]["dodslug"])
                
            
            enc(of_authors,[key, record["name"], slug, dob, dobslug, dod, dodslug])
        except Exception as e:
            handle_error([key, "general", str(e)])
    
    # general processing
    
    ml["key"] = max(len(key), ml["key"])
    numrecords = numrecords + 1
    if numrecords % 100000 == 0:
        print numrecords, "records processed"

print numrecords, "records processed"
print ml
simplejson.dump(ml, of_maxlengths)
