import datetime
import json
import os
import re
import psycopg2 as aligramdb

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask.helpers import url_for
from flask import session
from psycopg2.psycopg1 import connection, cursor
import uuid


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'aligram'
app.config['SECRET_KEY'] = 'itucsdb1622'

first_time_run_project = True

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/', methods=['GET', 'POST'])
def home_page():
    global first_time_run_project
    if first_time_run_project == True:
        session['loggedUser'] = None
        session['loggedUserID'] = None
        session['loginStatus'] = None
        first_time_run_project = False

    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT Username, Password FROM user_tb"""
        cursor.execute(query)
        data = cursor.fetchall()

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        exists = False
        for row in data:
            if username == row[0] and password == row[1]:
                exists = True

        if exists == False:
            error = 'Invalid Credentials. Please try again.'
            session['loggedUser'] = None
            session['loggedUserID'] = None
            session['loginStatus'] = None
        else:
            with aligramdb.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                cursor.execute("SELECT Id, Username FROM user_tb WHERE Username='%s'"%username)
                data = cursor.fetchall()

            user = data[0]
            session['loggedUser'] = user[1]
            session['loggedUserID'] = user[0]
            session['loginStatus'] = 'OK'

            return redirect(url_for('home_page'))
    now = datetime.datetime.now()
    return render_template('home.html', error=error, session=session['loginStatus'], current_time=now.ctime())

@app.route('/profile')
def profile_page():
    now = datetime.datetime.now()
    return render_template('profile_page.html', session=session['loginStatus'], current_time=now.ctime())

@app.route('/update_user', methods=['GET', 'POST'])
def update_user():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT Username FROM user_tb")
        data = cursor.fetchall()

    error = None
    if request.method == 'POST':
        new_username = request.form['username']
        exists = False
        for row in data:
            if new_username == row[0]:
                exists = True

        if exists == False:
            with aligramdb.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()

                cursor.execute("UPDATE user_tb SET Username='%s' WHERE ID='%s' "%(new_username, session['loggedUserID']))
                session['loggedUser'] = new_username

                return redirect(url_for('profile_page'))
        else:
            if new_username == session['loggedUser']:
                error = 'This new username that you entered is the same as your current username'
            else:
                error = 'the new username already exists'
    now = datetime.datetime.now()
    return render_template('update_user.html', error=error, current_time=now.ctime())

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():

    delete_message = None
    error = None
    if request.method == 'POST':
        with aligramdb.connect(app.config['dsn']) as connection:
            if(request.form['id'] == session['loggedUserID']):
                cursor = connection.cursor()

                cursor.execute("DELETE FROM user_tb WHERE ID='%s' "%(session['loggedUserID']))
                session['loggedUser'] = None
                session['loggedUserID'] = None
                session['loginStatus'] = None
                return redirect(url_for('home_page'))
            else:
                error = 'You entered wrong id'

    now = datetime.datetime.now()
    return render_template('delete_user.html', error=error, session=session['loggedUserID'], current_time=now.ctime())


@app.route('/register', methods=['GET', 'POST'])
def register():

    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT Username, Password FROM user_tb"""
        cursor.execute(query)
        data = cursor.fetchall()

    error = None
    if request.method == 'POST':

        username =  request.form['username']
        password = request.form['password']

        exists = False
        for row in data:
            if username == row[0] and password == row[1]:
                exists = True
        if exists:
            error = 'Username is in use! Please choose another username'

        else:

            with aligramdb.connect(app.config['dsn']) as connection:

                cursor = connection.cursor()
                query="""SELECT MAX(ID) FROM user_tb ID"""
                cursor.execute(query)
                data = cursor.fetchall()
                counter = str(int(data[0][0]) + 1)

                cursor.execute("INSERT INTO user_tb(ID, Username, Password) VALUES ('%s', '%s', '%s')"%(counter, username, password))

                connection.commit()

                return redirect(url_for('home_page'))

    return render_template('register.html', error=error)

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

@app.route('/DbCreate')
def create_tables_search():
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
def create_table_for_post():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query="""DROP TABLE IF EXISTS post_tb"""
        cursor.execute(query)

        query="""CREATE TABLE post_tb(ID INTEGER,MESSAGE VARCHAR(50))"""
        cursor.execute(query)

        query="""INSERT INTO post_tb(ID ,MESSAGE) VALUES (1,'First Post')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))

@app.route('/UserDbCreate')
def create_table_for_user():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS user_tb"""
        cursor.execute(query)

        query="""CREATE TABLE user_tb(ID VARCHAR(100) NOT NULL,Username VARCHAR(40), Password VARCHAR(10), Firstname VARCHAR(40),Lastname VARCHAR(40), Age int,Gender VARCHAR(10),Email VARCHAR(100), PRIMARY KEY (ID), UNIQUE(Username))"""
        cursor.execute(query)

        query="""INSERT INTO user_tb(ID ,Username, Password) VALUES (1,'kerim','test')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))

## Added by Adem(yenicead)
@app.route('/UserImages')
def create_table_for_user_images():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""DROP TABLE IF EXISTS images_tb"""
        cursor.execute(query)

        query="""CREATE TABLE images_tb(imageID INTEGER NOT NULL,imageName VARCHAR(50),imageContent VARCHAR(100))"""
        cursor.execute(query)

        query="""INSERT INTO images_tb(imageID ,imageName, imageContent) VALUES (1,'adem','yenice')"""
        cursor.execute(query)

        connection.commit()

        return redirect(url_for('home_page'))

# Added by Umut(umutyazgan)
@app.route('/Events')
def create_table_for_events():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""DROP TABLE IF EXISTS events_tb"""
        cursor.execute(query)

        query="""CREATE TABLE events_tb(ID INTEGER NOT NULL,eventName VARCHAR(50),eventDate VARCHAR(20),eventLocation VARCHAR(50))"""
        cursor.execute(query)

        query="""INSERT INTO events_tb(ID, eventName, eventDate, eventLocation) VALUES (1,'Birthday Party','09.12.2016','Not decided yet')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), True
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)



