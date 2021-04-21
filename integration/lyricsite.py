from urllib.parse import urlparse
from datetime import datetime
import json

use_mongo = True

try:
    import pymongo
except ImportError:
    import sqlite3
    import os
    use_mongo = False

class LyricSite:

    _base_url = None

    def __init__(self, base_url):
        result = urlparse(base_url)
        self._base_url = result.netloc

    def is_mine(self, url):
        result = urlparse(url)
        return result.netloc == self._base_url

    def fetch(self, url):
        pass

    def save_mongo(self, song, page):
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017")

        db = client.songs
        db.songs.insert_one({
            'url': song._url,
            'title': song._title,
            'lyric': song._lyric
        })
        payload = {
            'base_url': self._base_url
        }
        meta = db.song_meta.find(payload)
        if(meta.count() == 0):
            db.song_meta.insert_one({
                'base_url': self._base_url,
                'last_page': page,
                'last_song': song._url,
                'last_update': datetime.now(),
            })
        else:
            db.song_meta.replace_one(payload, {
                'base_url': self._base_url,
                'last_page': page,
                'last_song': song._url,
                'last_update': datetime.now()
            })

        client.close()

    def save_sqlite(self, song, page):
        # check if table exists
        db_name = 'lyric.db'
        
        if not os.path.isfile(db_name):
            # crate new db
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute('CREATE TABLE songs (id integer PRIMARY KEY AUTOINCREMENT, url text, title text, lyric text)')
            cur.execute('CREATE TABLE song_meta (id integer PRIMARY KEY AUTOINCREMENT, base_url text, last_url text, last_page integer, last_update date)')
            con.commit()
            con.close()
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("INSERT INTO songs (url, title, lyric) VALUES(?, ?, ?)", [song._url, song._title, song._lyric])
        con.commit()
        cur.execute("SELECT * FROM song_meta WHERE base_url = ?", [self._base_url])
        res = cur.fetchone()
        if res != None:
            cur.execute("UPDATE song_meta SET last_url = ?, last_update = ?, last_page = ?", [song._url, datetime.now(), page])
        else:
            cur.execute("INSERT INTO song_meta (base_url, last_url, last_page, last_update) VALUES (?, ?, ?, ?)", [self._base_url, song._url, page, datetime.now()])
        con.commit()
        con.close()

    def save(self, song, page):
        if use_mongo:
            self.save_mongo(song, page)
        else:
            self.save_sqlite(song, page)
    
    def getLastPageMongo(self):
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.songs
        meta = db.song_meta.find({
            'base_url': self._base_url
        })
        client.close()
        if(meta.count() == 0):
            return 1
        else:
            return meta[0]['last_page']

    def getLastPageSqlite(self):
        db_name = 'lyric.db'
        
        if not os.path.isfile(db_name):
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            # crate new db
            cur.execute('CREATE TABLE songs (id integer PRIMARY KEY AUTOINCREMENT, url text, title text, lyric text)')
            cur.execute('CREATE TABLE song_meta (id integer PRIMARY KEY AUTOINCREMENT, base_url text, last_url text, last_page integer, last_update date)')
            con.commit()
            con.close()
            return 1
        else:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM song_meta WHERE base_url = ?", [self._base_url])
            res = cur.fetchone()
            con.close()
            if res != None:
                return res['last_page']
            else:
                return 1

    def getLastPage(self):
        if use_mongo:
            return self.getLastPageMongo()
        else:
            return self.getLastPageSqlite()
        
    def isExistsMongo(self, url):
        client = MongoClient("mongodb://127.0.0.1:27017")
        db = client.songs
        song = db.songs.find({
            'url': url
        })
        return song.count() > 0

    def isExistsSqlite(self, url):
        db_name = 'lyric.db'
        
        if not os.path.isfile(db_name):
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            # crate new db
            cur.execute('CREATE TABLE songs (id integer PRIMARY KEY AUTOINCREMENT, url text, title text, lyric text)')
            cur.execute('CREATE TABLE song_meta (id integer PRIMARY KEY AUTOINCREMENT, base_url text, last_url text, last_page integer, last_update date)')
            con.commit()
            return False
        else:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute("SELECT * FROM songs WHERE url = ?", [url])
            res = cur.fetchone()
            return res != None

    def isExists(self, url):
        if use_mongo:
            return self.isExistsMongo(url)
        else:
            return self.isExistsSqlite(url)
        
        