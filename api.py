from flask import Flask, jsonify
from flask.ext import restful
from flask import g #sqlite connection

import sqlite3

import datetime
import sqlite3


app = Flask(__name__)
api = restful.Api(app)

DATABASE = 'xbee_rssi.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
    return db


@app.route('/')
def index():
    return "Data is at: <b>/api/v1.0/INTEGER</b>"

class RSSIData(restful.Resource):
    def get(self,update_lim):
        cur = get_db().cursor()
        sql = 'SELECT * FROM signal ORDER BY date DESC LIMIT %s' % (update_lim)
	cur.execute(sql)
	result =  cur.fetchall()
        date = []
	xbee = []
	rssi = []

	for pt in result:
    	    date.append(pt[0])
    	    xbee.append(pt[1])
            rssi.append(pt[2]) 

	#df = psql.read_frame(sql,conn)
        result_dict = {'date':date,'rssi':rssi,'xbee':xbee}
        return jsonify(result_dict)


api.add_resource(RSSIData, '/api/v1.0/<string:update_lim>')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
