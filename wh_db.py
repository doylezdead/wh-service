__author__ = 'rcdoyle'

import pymongo
import time
import re
import newspaper
from wh_lib import top_keywords, find_syns

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
        blob['keywords'] = top_keywords(blob['text'])
        if len(blob['keywords']) == 0:
            return
        print blob['title']

        artcol = self.client['mh']['articles']
        artcol.insert_one(blob)
        return

    def get_best_match(self, word):

        # find synonyms
        # iterate synonyms and match articles.
        # articles that appear the most are chosen as best match

        word = word.lower()
        synlist = find_syns(word)
        relate_dict = {}

        artcol = self.client['mh']['articles']
        queryresult = artcol.find({'keywords': {'$in': [word]}})
        for art in queryresult:
            relate_dict[art['_id']] = 3

        for syn in synlist:
            synqueryresult = artcol.find({'keywords': {'$in': [syn]}})
            for art in synqueryresult:
                if art['_id'] in relate_dict:
                    relate_dict[art['_id']] += 1
                else:
                    relate_dict[art['_id']] = 1

        keys = relate_dict.keys()
        values = relate_dict.values()
        max_index = array_max_index(values)
        best_id = keys[max_index]

        best_article = artcol.find({'_id':best_id})

        best_article.pop('text')
        best_article.pop('keywords')
        return best_article



def array_max_index(array):
    max_val = -1
    max_index = -1
    for index in range(len(array)):
        if array[index] > max_val:
            max_val = array[index]
            max_index = index
    return max_index



