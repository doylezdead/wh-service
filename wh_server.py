from bottle import Bottle, response, request
import json
import wh_db as whdb
import subprocess as sp
import os
import signal
import sys
import wh_lib

app = Bottle()

def signal_handler(signal, frame):
    print('shutting down mongod...')
    mongo_proc.send_signal(15)
    print('shutting down cpunch server...')
    sys.exit(0)
try:
    os.makedirs(os.path.expanduser('~/.wh/db'))
except OSError:
    pass
mongo_args = ['mongod', '--logpath', os.path.expanduser('~/.wh/mongolog'), '--bind_ip',
              '127.0.0.1', '--port', '29292', '--dbpath', os.path.expanduser('~/.wh/db')]
mongo_proc = sp.Popen(mongo_args)
signal.signal(signal.SIGINT, signal_handler)

dbuser = whdb.DBUser(port=29292)         # create a new dbuser instance to start handling the data package

@app.hook('after_request')
def enable_cors():

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'


@app.route('/synonym/', method='GET')
def handle_request_for_synonym():
    raw_return = request.GET.get('word')

    send_pack = wh_lib.find_syns(raw_return)

    raw_send = json.dumps(send_pack)
    return raw_send

@app.route('/articles/', method='GET')
def handle_request_for_articles():
    raw_return = request.GET.get('word')

    best = dbuser.get_best_match(raw_return)
    highest = dbuser.get_highest_rated()
    rand = dbuser.get_random_article()

    if best != False:
        send_pack = [best, highest, rand]
    else:
        send_pack = [highest, rand]

    raw_send = json.dumps(send_pack)
    return raw_send

@app.route('/rate/', method='GET')
def handle_request_to_rate():
    article_to_rate = request.GET.get('article')
    rating = request.GET.get('value')
    if -1 > rating > 1:
        return 'booooo'

    raw_send = json.dumps(dbuser.rate(article_to_rate, rating))

    return raw_send

print('Ctrl-C to gracefully shut down server')
app.debug = True
app.run(host='0.0.0.0', port=60606)
