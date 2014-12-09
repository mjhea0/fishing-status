import csv
import sqlite3


db_filename = 'profit.db'
data_filename = 'linky.csv'


CREATE = """CREATE TABLE links(
                id INTEGER PRIMARY KEY, name TEXT, url TEXT, category TEXT)"""


SQL = """INSERT INTO links(name, url, category)
            VALUES (:name, :url, :category)"""


with open(data_filename, 'rU') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        conn.text_factory = str
        cursor.executemany(SQL, csv_reader)
