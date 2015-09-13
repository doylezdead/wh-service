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

@app.route('/synonym/', method='GET')
def handle_request_for_synonym():
    raw_return = request.GET.get('word')

    send_pack = wh_lib.find_syns(raw_return)

    raw_send = json.dumps(send_pack)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return raw_send

@app.route('/articles/', method='GET')
def handle_request_for_articles():
    raw_return = request.GET.get('word')

    send_pack = dbuser.get_best_match(raw_return)

    raw_send = json.dumps(send_pack)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    return raw_send

@app.route('/articles', method='POST')
def handle_request_for_insert():
    raw_return = request.body.readline()
    return_pack = json.loads(raw_return.decode('utf-8'))

    send_pack = dbuser.user_insert(return_pack)

    raw_send = json.dumps(send_pack).encode('utf-8')

    return raw_send

print('Ctrl-C to gracefully shut down server')
app.debug = True
app.run(host='0.0.0.0', port=60606)
