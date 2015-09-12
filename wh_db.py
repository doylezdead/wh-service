__author__ = 'rcdoyle'

import pymongo
import time
import re
import newspaper

class DBUser:

    def __init__(self, port=29292):
        self.client = pymongo.MongoClient('localhost', port)
        self.authenticated = False

    # example of inserting a document into the 'user' database, 'info' collection
    def _register_user(self):

        data = {'username': 'herpmahderp',
                'address': '1234 Rain St.',
                'gender': 'male'}

        db = self.client['people']
        infocol = db['info']

        infocol.insert_one(data)
        # infocol.find(query) to find objects in the db
        return {'message': 'successfully registered user ' + data['user']}

    def fetch_articles(self, obj):
        return {0: 0}

    def user_insert(self, obj):
        artcol = self.client['mh']['articles']

        artcol.insertone({})
        return

    def insert_article(self, article):
        assert type(article) is newspaper.Article
        blob = {}
        for attr in ('title', 'text', 'keywords', 'summary', 'url'):
            blob[attr] = getattr(article, attr)
            blob['time'] = time.time()
            blob['rating'] = 0
            print blob['title']

        artcol = self.client['mh']['articles']
        artcol.insert_one(blob)
        return

