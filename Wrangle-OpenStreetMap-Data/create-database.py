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

cursor.execute('''
               DROP TABLE IF EXISTS nodes_tags''')
connect.commit()

cursor.execute('''
               DROP TABLE IF EXISTS ways''')
connect.commit()

cursor.execute('''
               DROP TABLE IF EXISTS ways_tags''')
connect.commit()

cursor.execute('''
               DROP TABLE IF EXISTS ways_nodes''')
connect.commit()

# Create table "nodes"
# Create tables based on pre-defined scherma
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
              i['changeset'], i['timestamp'])
             for i in dr]

# Insear the formatted data
cursor.executemany('''INSERT INTO nodes(id, lat, lon, user, uid, version,
                   changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);''',
                   to_db)
connect.commit()

# Create table "nodes_tags"
cursor.execute('''
        CREATE TABLE nodes_tags (
        id INTEGER,
        key TEXT,
        value TEXT,
        type TEXT,
        FOREIGN KEY (id) REFERENCES nodes(id)
        );
''')
connect.commit()

with open('nodes_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),
              i['value'].decode('utf-8'), i['type'].decode('utf-8'))
             for i in dr]

cursor.executemany('''INSERT INTO nodes_tags(id, key, value, type)
                       VALUES (?, ?, ?, ?);''', to_db)
connect.commit()

# Create table "ways"
cursor.execute('''
        CREATE TABLE ways (
        id INTEGER PRIMARY KEY NOT NULL,
        user TEXT,
        uid INTEGER,
        version TEXT,
        changeset INTEGER,
        timestamp TEXT
        );
''')
connect.commit()

with open('ways.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['user'].decode('utf-8'),
              i['uid'].decode('utf-8'), i['version'].decode('utf-8'),
              i['changeset'].decode('utf-8'), i['timestamp'].decode('utf-8'))
             for i in dr]
cursor.executemany('''INSERT INTO ways(
                   id, user, uid, version, changeset, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)''', to_db)
connect.commit()

# Create table "ways_tags"
cursor.execute('''
        CREATE TABLE ways_tags (
        id INTEGER NOT NULL,
        key TEXT NOT NULL,
        value TEXT NOT NULL,
        type TEXT,
        FOREIGN KEY (id) REFERENCES ways(id)
        );
''')
connect.commit()

with open('ways_tags.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['key'].decode('utf-8'),
              i['value'].decode('utf-8'), i['type'].decode('utf-8'))
             for i in dr]

cursor.executemany('''INSERT INTO ways_tags(
                   id, key, value, type)
                   VALUES (?, ?, ?, ?)''', to_db)
connect.commit()

# Create table ways_nodes

cursor.execute('''
        CREATE TABLE ways_nodes (
        id INTEGER NOT NULL,
        node_id INTEGER NOT NULL,
        position INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES ways(id),
        FOREIGN KEY (node_id) REFERENCES nodes(id)
        );
''')
connect.commit()

with open('ways_nodes.csv', 'rb') as f:
    dr = csv.DictReader(f)
    to_db = [(i['id'].decode('utf-8'), i['node_id'].decode('utf-8'),
              i['position'].decode('utf-8')) for i in dr]

cursor.executemany('''INSERT INTO ways_nodes(
                   id, node_id, position)
                   VALUES (?, ?, ?)''', to_db)
connect.commit()
connect.close()
