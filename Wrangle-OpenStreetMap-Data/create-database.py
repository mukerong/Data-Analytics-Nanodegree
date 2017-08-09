# Import the modules
import csv
import sqlite3
from pprint import pprint


# Connect to the database and create a cursor object
sqlite_file = 'osm_chicago.db'
connect = sqlite3.connect(sqlite_file)
cursor = connect.cursor()

# Drop the table if exists
cursor.execute('''
               DROP TABLE IF EXISTS nodes
''')

# Create tables based on pre-defined schema
cursor.execute('''
        CREATE TABLE nodes (
        id INTEGER PRIMARY KEY NOT NULL,
        lat REAL,
        lon REAL,
        user TEXT,
        uid INTEGER,
        version INTEGER,
        changeset INTEGER,
        timestamp TEXT
        );
''')

# Commit the change
connect.commit()

# Read the csv file as a dictionary, format the data as a list of tuples
with open('nodes.csv', 'rt', encoding='utf8') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp'])
             for i in dr]
