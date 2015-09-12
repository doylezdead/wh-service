import PyDictionary
import newspaper
import wh_db as whdb

def find_syns(word):
    dict = PyDictionary.PyDictionary()
    return {'syns': dict.synonym(word)}

def import_articles(sitelist):
    imported_sitelist = []
    dbuser = whdb.DBUser(port=29292)
    for site in sitelist:
        # populate sitelist
        imported_sitelist.append(newspaper.build(site))

    for site in imported_sitelist:
        for article in site.articles:
            article.download()
            article.parse()
            dbuser.insert_article(article)
