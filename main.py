#!/usr/bin/python
import psycopg2
import sys
from sys import stdout
import abbr_dict
 
def main():

    try:
        conn_string = "host='localhost' dbname='osm_test' user='postgres' password=''"
        conn = psycopg2.connect(conn_string)
	print("Connected to database!")
    except:    
        print("Unable to connecto to database: {}".format(conn_string))

    #def osm tables
    osm_tables = {'osm_motorways',	#(optional)
		  'osm_mainroads',
		  'osm_minorroads',
		  'osm_motorways_gen0',	#(optional)
		  'osm_motorways_gen1',	#(optional)
		  'osm_mainroads_gen0',
		  'osm_mainroads_gen1'}

    #def psql cursor
    cursor = conn.cursor()

    #select dict
    language_abbreviations = abbr_dict.abbreviations.get('dutch')

    #loop through osm_tables
    for osm_table in osm_tables:
	print("\nUpdating OSM Table: {}".format(osm_table))
	
	for language_abbreviation in language_abbreviations:
		regex_match = language_abbreviation.get('match')
		regex_replace = language_abbreviation.get('replace')
		print("\tExecuting \"UPDATE {} SET name = regexp_replace(name, '{}', '{}', 'g');\" ".format(osm_table, regex_match, regex_replace)),
		stdout.flush()
		try:
		    update_query = "UPDATE %s" % (osm_table,) + " SET name = regexp_replace(name, %s, %s, 'g');"
		    cursor.execute(update_query, (regex_match, regex_replace))
		    conn.commit()
		    print("done!")
		except Exception as error:
		    print("error! {}".format(error))

    if conn:
	conn.close()    

    print("\nDone updating OSM table(s)")

if __name__ == "__main__":
    main()
