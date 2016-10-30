import datetime
import json
import os
import re
import psycopg2 as aligramdb

from flask import Flask
from flask import render_template
from flask import redirect
from flask.helpers import url_for
from psycopg2.psycopg1 import connection, cursor



app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/profile')
def profile_page():
    now = datetime.datetime.now()
    return render_template('profile_page.html', current_time=now.ctime())

@app.route('/friends')
def friends_page():
    now = datetime.datetime.now()
    return render_template('friends_page.html', current_time=now.ctime())

@app.route('/myGallery')
def myGallery():
    now = datetime.datetime.now()
    return render_template('myGallery.html', current_time=now.ctime())

@app.route('/search')
def search():
    now = datetime.datetime.now()
    return render_template('search.html', current_time=now.ctime())

@app.route('/post')
def post():
    now = datetime.datetime.now()
    return render_template('post.html', current_time=now.ctime())

@app.route('/searchDbCreate')
def create_table_for_search():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""DROP TABLE IF EXISTS SEARCH"""
        cursor.execute(query)

        query="""CREATE TABLE SEARCH(ID INTEGER,WORD VARCHAR(15))"""
        cursor.execute(query)

        query="""INSERT INTO SEARCH(ID ,WORD) VALUES (1,'DENEME')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))

@app.route('/postTable')
def create_table_for_search():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""DROP TABLE IF EXISTS POST"""
        cursor.execute(query)

        query="""CREATE TABLE POST(ID INTEGER,MESSAGE VARCHAR(50), USER VARCHAR(50))"""
        cursor.execute(query)

        query="""INSERT INTO POST(ID ,WORD,USER) VALUES (1,'First Post','Berhak')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)



