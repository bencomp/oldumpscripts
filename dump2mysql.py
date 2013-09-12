#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
import re, simplejson, sys
import logging


# Configuration of fields
edition_string_fields = ["key","title","subtitle","physical_format","physical_dimensions","weight","number_of_pages","publish_date","publish_country","edition_name","by_statement"]
edition_strlist_fields = ["publishers","publish_places"]
edition_reflist_fields = ["works","authors"]

insert_basics = "INSERT INTO editions (olid, title, subtitle, edition_name, first_work, first_author, by_statement, first_publisher, first_publishplace, publish_country, publication_year, format, dimensions, weight, num_pages) VALUES (%(key)s, %(title)s, %(subtitle)s, %(edition_name)s, %(works)s, %(authors)s, %(by_statement)s, %(publishers)s, %(publish_places)s, %(publish_country)s, %(publish_date)s, %(physical_format)s, %(physical_dimensions)s, %(weight)s, %(number_of_pages)s)"
insert_publishers = "INSERT INTO editions_publishers (e_key, n, publisher) VALUES (%s, %s, %s)"
insert_publish_places = "INSERT INTO editions_publish_places (e_key, n, publish_place) VALUES (%s, %s, %s)"
insert_works = "INSERT INTO editions_works (e_key, n, w_key) VALUES (%s, %s, %s)"
insert_authors = "INSERT INTO editions_authors (e_key, n, a_key) VALUES (%s, %s, %s)"
insert_languages = "INSERT INTO editions_languages (e_key, n, language) VALUES (%s, %s, %s)"
insert_isbn10 = "INSERT INTO editions_isbn10 (e_key, n, isbn10) VALUES (%s, %s, %s)"
insert_isbn13 = "INSERT INTO editions_isbn13 (e_key, n, isbn13) VALUES (%s, %s, %s)"
insert_lccn = "INSERT INTO editions_lccn (e_key, n, lccn) VALUES (%s, %s, %s)"
insert_lc_classification = "INSERT INTO editions_lc_classification (e_key, n, lc_classification) VALUES (%s, %s, %s)"
insert_ddc = "INSERT INTO editions_ddc (e_key, n, ddc) VALUES (%s, %s, %s)"
insert_contributors = "INSERT INTO editions_contributors (e_key, n, role, name) VALUES (%s, %s, %s, %s)"
insert_identifiers = "INSERT INTO editions_identifiers (e_key, n, id_type, identifier) VALUES (%s, %s, %s, %s)"
insert_classifications = "INSERT INTO editions_classifications (e_key, n, classification_type, classification) VALUES (%s, %s, %s, %s)"

pattern = re.compile('^[^{]*')


def insert_e_main(r):
    """Insert an Edition record's basic information.
    """
    
    
    data_basics = {}
    for key in edition_string_fields:
        if key in r.keys():
            data_basics[key] = r[key]
        else:
            data_basics[key] = None
    
    for key in edition_strlist_fields:
        if key in r.keys():
            data_basics[key] = r[key][0]
        else:
            data_basics[key] = None
            
    for key in edition_reflist_fields:
        if key in r.keys():
            data_basics[key] = r[key][0]["key"]
        else:
            data_basics[key] = None
    
    cursor.execute(insert_basics, data_basics)
    
    if "publishers" in r.keys():
        n = 0
        for p in r["publishers"]:
            n = n + 1
            data_publishers = (r["key"], n, p)
            cursor.execute(insert_publishers, data_publishers)
            
    if "publish_places" in r.keys():
        n = 0
        for p in r["publish_places"]:
            n = n + 1
            data_publish_places = (r["key"], n, p)
            cursor.execute(insert_publish_places, data_publish_places)
            
    if "authors" in r.keys():
        n = 0
        for p in r["authors"]:
            n = n + 1
            data_authors = (r["key"], n, p["key"])
            cursor.execute(insert_authors, data_authors)
    
    if "works" in r.keys():
        n = 0
        for p in r["works"]:
            n = n + 1
            data_works = (r["key"], n, p["key"])
            cursor.execute(insert_works, data_works)
    
    if "languages" in r.keys():
        n = 0
        for p in r["languages"]:
            n = n + 1
            data_languages = (r["key"], n, p["key"])
            cursor.execute(insert_languages, data_languages)
    
    if "isbn_10" in r.keys():
        n = 0
        for p in r["isbn_10"]:
            n = n + 1
            data_isbn10 = (r["key"], n, p)
            cursor.execute(insert_isbn10, data_isbn10)
            
    if "isbn_13" in r.keys():
        n = 0
        for p in r["isbn_13"]:
            n = n + 1
            data_isbn13 = (r["key"], n, p)
            cursor.execute(insert_isbn13, data_isbn13)
            
    if "lccn" in r.keys():
        n = 0
        for p in r["lccn"]:
            n = n + 1
            data_lccn = (r["key"], n, p)
            cursor.execute(insert_lccn, data_lccn)
            
    if "lc_classifications" in r.keys():
        n = 0
        for p in r["lc_classifications"]:
            n = n + 1
            data_lc_classifications = (r["key"], n, p)
            cursor.execute(insert_lc_classification, data_lc_classifications)
            
    if "dewey_decimal_class" in r.keys():
        n = 0
        for p in r["dewey_decimal_class"]:
            n = n + 1
            data_ddc = (r["key"], n, p)
            cursor.execute(insert_ddc, data_ddc)
            
    if "contributors" in r.keys():
        n = 0
        for p in r["contributors"]:
            n = n + 1
            data_contributors = (r["key"], n, p["role"], p["name"])
            cursor.execute(insert_contributors, data_contributors)
            
    if "identifiers" in r.keys() and len(r["identifiers"]) > 0:
        for k in r["identifiers"].keys():
            n = 0
            for p in r["identifiers"][k]:
                n = n + 1
                data_id = (r["key"], n, k, p)
                cursor.execute(insert_identifiers, data_id)
            
    if "classifications" in r.keys() and len(r["classifications"]) > 0:
        for k in r["classifications"].keys():
            n = 0
            for p in r["classifications"][k]:
                n = n + 1
                data_classifications = (r["key"], n, k, p)
                cursor.execute(insert_classifications, data_classifications)
            
logging.basicConfig(filename='dump2mysql.log',level=logging.DEBUG)

pwfile = open("dump2mysqlpw.txt")
[u, p] = pwfile.next().split()
cnx = mysql.connector.connect(user=u, password=p,
                              host='localhost',
                              database='openlibrary')
                              
cursor = cnx.cursor()
counter = 0

for line in open("../ol_dump_2013-08-31.txt"):
    
    try:
        l2 = re.sub(pattern, "", line)
        record = simplejson.loads(l2)
        if record["key"][0:6] == "/books" and record["type"]["key"] == "/type/edition":
            insert_e_main(record)
            counter = counter + 1
            if counter % 50000 == 0:
                print counter, "editions done"
                cnx.commit()
    
    except Exception as e:
        #print sys.exc_info()
        logging.exception("%s %s" % (record["key"], e))
        print record["key"]
        print e
        #line.encode('ascii', 'backslashreplace')
        #l2.encode('ascii', 'backslashreplace')
        

cursor.close()
cnx.close()