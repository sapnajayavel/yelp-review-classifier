import json
import sqlite3

DATA_FILENAME_FORMAT = 'yelp_phoenix_academic_dataset/yelp_academic_dataset_{}.json'

def create_db():
    db = sqlite3.connect("new_yelp.sqlite")
    c = db.cursor()

    c.execute('''CREATE TABLE business(
                   business_id  TEXT PRIMARY KEY,
                   name         TEXT,
                   stars        REAL,
                   review_count INTEGER
                 )''')

    c.execute('''CREATE TABLE user(
                   user_id       TEXT PRIMARY KEY,
                   name          TEXT,
                   review_count  INTEGER,
                   average_stars REAL,
                   funny         INTEGER,
                   useful        INTEGER,
                   cool          INTEGER
                 )''')

    c.execute('''CREATE TABLE review(
                   id          INTEGER PRIMARY KEY,
                   business_id TEXT,
                   user_id     TEXT,
                   stars       REAL,
                   text        TEXT,
                   date        TEXT,
                   funny       INTEGER,
                   useful      INTEGER,
                   cool        INTEGER,
                   FOREIGN KEY(business_id) REFERENCES business(business_id),
                   FOREIGN KEY(user_id) REFERENCES user(user_id)
                 )''')

    db.commit()
    db.close()

def insert_businesses(cursor):
    with open(DATA_FILENAME_FORMAT.format('business'), 'r') as f:
        for line in f: 
            business = json.loads(line.strip())

            values = [] 
            values.append(business['business_id'])
            values.append(business['name'])
            values.append(business['stars'])
            values.append(business['review_count'])

            cursor.execute("INSERT INTO business VALUES (?,?,?,?)", values)

def insert_users(cursor):
    with open(DATA_FILENAME_FORMAT.format('user'), 'r') as f:
        for line in f: 
            user = json.loads(line.strip())

            values = [] 
            values.append(user['user_id'])
            values.append(user['name'])
            values.append(user['review_count'])
            values.append(user['average_stars'])
            values.append(user['votes']['funny'])
            values.append(user['votes']['useful'])
            values.append(user['votes']['cool'])

            c.execute("INSERT INTO user VALUES (?,?,?,?,?,?,?)", values)

def insert_reviews(cursor):
    with open(DATA_FILENAME_FORMAT.format('review'), 'r') as f:
        i = 1
        for line in f: 
            review = json.loads(line.strip())

            values = [] 
            values.append(i)
            values.append(review['business_id'])
            values.append(review['user_id'])
            values.append(review['stars'])
            values.append(review['text'])
            values.append(review['date'])
            values.append(review['votes']['funny'])
            values.append(review['votes']['useful'])
            values.append(review['votes']['cool'])

            c.execute("INSERT INTO review VALUES (?,?,?,?,?,?,?,?,?)", values)

            i += 1

if __name__ == "__main__":
    db = sqlite3.connect("new_yelp.sqlite")
    c = db.cursor()

    c.execute("DELETE FROM business")
    c.execute("DELETE FROM user")
    c.execute("DELETE FROM review")

    insert_businesses(c)
    insert_users(c)
    insert_reviews(c)

    c.execute("CREATE INDEX review_useful ON review(useful)")

    db.commit()
    db.close()
