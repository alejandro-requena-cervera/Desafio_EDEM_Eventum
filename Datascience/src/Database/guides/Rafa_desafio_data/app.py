from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras
import pandas as pd
from datetime import datetime as dt
from decouple import config


app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello, World!'


@app.route('/eventData', methods=['GET'])
def get_event_data():

    name = config('RENDER_DB_USER')
    pswrd = config('RENDER_DB_PASS')
    hostname = config('RENDER_DB_HOST')
    portid = config('RENDER_DB_PORT')
    db = config('RENDER_DB_DB') 
    conn = None
    
    with psycopg2.connect(
        host = hostname, 
        dbname = db,
        user = name,
        password = pswrd,
        port = portid) as conn:
    
        with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cur:
            q_title = 'SELECT * FROM "Facilities";'
            cur.execute(q_title)
            respuesta = cur.fetchall()
    
    return respuesta

if __name__ == '__main__':
    app.run(debug=True)


