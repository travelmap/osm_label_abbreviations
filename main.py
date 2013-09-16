#!/usr/bin/python
import argparse
import psycopg2
import sys
from sys import stdout
import abbr_dict
 
def main():

    #get required args from commandline
    parser = argparse.ArgumentParser(description='OSM label abbreviations')
    parser.add_argument('-d','--db', help='Database name. Example; osm_amsterdam',required=True)
    parser.add_argument('-l','--language', help='Language to apply. Supported; [catalan, czech, danish, dutch, english, french, german, italian, portugese, russian, spanish, swedish, turkish]', required=True)
    args = parser.parse_args()

    #select dict
    language_abbreviations = abbr_dict.abbreviations.get(args.language)
    if language_abbreviations == None:
        sys.exit("Language '"+args.language+"' not yet supported")

    #connect to database
    try:
        conn_string = "host='localhost' dbname='"+args.db+"' user='postgres' password=''"
        conn = psycopg2.connect(conn_string)
	print("Connected to database!")
    except:    
	sys.exit("Unable to connect to to database: {}".format(conn_string))

    #def psql cursor
    cursor = conn.cursor()

    #def osm tables
    osm_tables = {'osm_motorways',	#(optional)
		  'osm_mainroads',
		  'osm_minorroads',
		  'osm_motorways_gen0',	#(optional)
		  'osm_motorways_gen1',	#(optional)
		  'osm_mainroads_gen0',
		  'osm_mainroads_gen1'}

    #loop through osm_tables
    for osm_table in osm_tables:
	print("\nUpdating OSM Table: {}".format(osm_table))
	
	for language_abbreviation in language_abbreviations:
		regex_match = language_abbreviation.get('match')
		regex_replace = language_abbreviation.get('replace')
		print("\tExecuting \"UPDATE {} SET name = regexp_replace(name, '{}', '{}', 'gi');\" ".format(osm_table, regex_match, regex_replace)),
		stdout.flush()
		try:
		    update_query = "UPDATE %s" % (osm_table,) + " SET name = regexp_replace(name, %s, %s, 'gi');"
		    cursor.execute(update_query, (regex_match, regex_replace))
		    conn.commit()
		    print("done!")
		except Exception as error:
		    sys.exit("error! {}".format(error))

    if conn:
	conn.close()    

    print("\nDone updating OSM table(s)")

if __name__ == "__main__":
    main()
