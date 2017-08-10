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
               DROP TABLE IF EXISTS nodes''')
connect.commit()

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
with open('nodes.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['lat'].decode('utf-8'),
              i['lon'].decode('utf-8'), i['user'].decode('utf-8'),
              i['uid'].decode('utf-8'), i['version'].decode('utf-8'),
              i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8'))
             for i in dr]

# Insear the formatted data
cursor.executemany('''INSERT INTO nodes(id, lat, lon, user, uid, version,
                   changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                   to_db)
connect.commit()
