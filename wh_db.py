__author__ = 'rcdoyle'

import pymongo
from bson.objectid import ObjectId
import time
import random
import newspaper
from wh_lib import top_keywords, find_syns, get_site, strip_title

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
        artcol = self.client['mh']['articles']
        #check and see if its already in
        query = artcol.find({'title': article.title})
        if query.count() > 0:
            return str(query[0]['_id'])

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

        artcol.insert_one(blob)
        return str(blob['_id'])

    def get_best_match(self, w):

        # find synonyms
        # iterate synonyms and match articles.
        # articles that appear the most are chosen as best match

        w = w.lower()
        splitword = w.split(' ')
        synlist = []

        for word in splitword:
            synlist.extend(find_syns(word))

        relate_dict = {}

        artcol = self.client['mh']['articles']

        for word in splitword:
            queryresult = artcol.find({'keywords': {'$in': [word]}})
            for art in queryresult:
                if str(art['_id']) in relate_dict:
                    relate_dict[str(art['_id'])] += 3
                else:
                    relate_dict[str(art['_id'])] = 3

        for syn in synlist:
            synqueryresult = artcol.find({'keywords': {'$in': [syn]}})
            for art in synqueryresult:
                if str(art['_id']) in relate_dict:
                    relate_dict[str(art['_id'])] += 1
                else:
                    relate_dict[str(art['_id'])] = 1

        keys = relate_dict.keys()
        values = relate_dict.values()
        max_index = array_max_index(values)
        if max_index < 0:
            return False
        best_id = keys[max_index]

        best_article = artcol.find({'_id': ObjectId(best_id)})[0]

        best_article.pop('text')
        best_article.pop('keywords')
        best_article['_id'] = str(best_article['_id'])
        best_article['site'] = get_site(best_article['url'])
        best_article['title'] = strip_title(best_article['title'])
        return best_article

    def get_random_article(self):
        artcol = self.client['mh']['articles']
        colsize = artcol.count()
        randart = artcol.find()[random.randrange(colsize)]
        randart.pop('text')
        randart.pop('keywords')
        randart['_id'] = str(randart['_id'])
        randart['site'] = get_site(randart['url'])
        randart['title'] = strip_title(randart['title'])
        return randart

    def get_highest_rated(self):
        artcol = self.client['mh']['articles']
        highest = artcol.find_one(sort=[("rating", -1)])
        highest.pop('text')
        highest.pop('keywords')
        highest['_id'] = str(highest['_id'])
        highest['site'] = get_site(highest['url'])
        highest['title'] = strip_title(highest['title'])
        return highest

    def rate(self, uid, inc):
        artcol = self.client['mh']['articles']
        artcol.update({'_id': ObjectId(uid)}, {'$inc': {'rating': int(inc)}})
        newvalue = artcol.find_one({'_id': ObjectId(uid)})['rating']
        return newvalue

def array_max_index(array):
    max_val = -1
    max_index = -1
    for index in range(len(array)):
        if array[index] > max_val:
            max_val = array[index]
            max_index = index
    return max_index
