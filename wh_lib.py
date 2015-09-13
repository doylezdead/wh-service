import PyDictionary
import newspaper
import wh_db as whdb
from topia.termextract import extract

extractor = extract.TermExtractor()

def find_syns(word):
    dict = PyDictionary.PyDictionary()
    return {'syns': dict.synonym(word)}

def import_articles(sitelist):
    imported_sitelist = []
    dbuser = whdb.DBUser(port=29292)
    count = 0
    for site in sitelist:
        # populate sitelist
        imported_sitelist.append(newspaper.build(site))

    for site in imported_sitelist:
        for article in site.articles:
            article.download()
            article.parse()
            dbuser.insert_article(article)
            count += 1
            print count
            if count == 1000:
                break

    return count

def top_keywords(self, text):
    retlist = []
    count = 0
    for item in sorted(extractor(text)):
        retlist.append(item[0])
        count += 1
        if count == 10:
            break
