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


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    #user, password, host, _, dbname = match.groups()
    #dsn = """user='{}' password='{}' host='{}'
    #         dbname='{}'""".format(user, password, host, dbname)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn

@app.route('/', methods=['GET', 'POST'])
def home_page():

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
    try:
        return render_template('home.html', error=error, session=session['loginStatus'], current_time=now.ctime())
    except:
        return render_template('home.html', error=error, session=None, current_time=now.ctime())

@app.route('/profile')
def profile_page():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT Social_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
        data = cursor.fetchall()

        social_id = None

        if len(data) > 0:
            social_id = data[0][0]

        facebook_acc = ''
        twitter_acc = ''
        instagram_acc = ''

        if social_id != None:
            cursor.execute("SELECT facebook, twitter, instagram FROM social_accounts_tb WHERE ID = '%s' "%social_id)
            data = cursor.fetchall()

            facebook_acc = data[0][0]
            twitter_acc = data[0][1]
            instagram_acc = data[0][2]


    now = datetime.datetime.now()
    return render_template('profile_page.html', session=session['loginStatus'], facebook = facebook_acc, twitter = twitter_acc, instagram = instagram_acc, current_time=now.ctime())

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

@app.route('/social_accounts', methods=['GET', 'POST'])
def social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT Social_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
        data = cursor.fetchall()

        error = None
        if request.method == 'POST':

            facebook_acc = request.form['facebook account']
            twitter_acc = request.form['twitter account']
            instagram_acc = request.form['instagram account']
            if len(data) > 0:
                if data[0][0] == None:
                    cursor.execute("INSERT INTO social_accounts_tb(facebook, twitter, instagram) VALUES ('%s', '%s', '%s') RETURNING id"%(facebook_acc, twitter_acc, instagram_acc))
                    
                    cursor.execute("SELECT lastval()")
                    social_id = cursor.fetchall()
                    social_id = social_id[0][0]
                    
                    cursor.execute("UPDATE user_tb SET Social_ID = '%d' WHERE Username = '%s' "%(social_id, session['loggedUser']))
                
                else:
                    cursor.execute("UPDATE social_accounts_tb SET facebook ='%s', twitter = '%s', instagram = '%s' WHERE ID='%s' "%(facebook_acc, twitter_acc, instagram_acc, data[0][0]))
                return redirect(url_for('profile_page'))

    now = datetime.datetime.now()
    return render_template('social_accounts.html', current_time=now.ctime())

@app.route('/remove_social_accounts', methods=['GET', 'POST'])
def remove_social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        if request.method == 'POST':
            cursor.execute("SELECT Social_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
            data = cursor.fetchall()
            if len(data) > 0:
                print ('i am in')
                if data[0][0] != None:
                    cursor.execute("DELETE FROM social_accounts_tb WHERE ID = '%d' "%int(data[0][0]))
                    return redirect(url_for('profile_page'))
        
    now = datetime.datetime.now()
    return render_template('remove_social_accounts.html', current_time=now.ctime())

@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():

    delete_message = None
    error = None
    if request.method == 'POST':
        with aligramdb.connect(app.config['dsn']) as connection:
            if(int(request.form['id']) == session['loggedUserID']):
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
            if username == row[0]:
                exists = True
        if exists:
            error = 'Username is in use! Please choose another username'

        else:

            with aligramdb.connect(app.config['dsn']) as connection:

                cursor = connection.cursor()

                cursor.execute("INSERT INTO user_tb(Username, Password) VALUES ('%s', '%s')"%(username, password))

                connection.commit()

                return redirect(url_for('home_page'))

    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session['loggedUser'] = None
    session['loggedUserID'] = None
    session['loginStatus'] = None    

    return redirect(url_for('home_page'))

@app.route('/friends')
def friends_page():
    now = datetime.datetime.now()
    return render_template('friends_page.html', current_time=now.ctime())

@app.route('/myGallery')
def myGallery():
    now = datetime.datetime.now()
    return render_template('myGallery.html', current_time=now.ctime())

@app.route('/search', methods=['GET', 'POST'])
def search():
    message=" "

    if request.method == 'POST':
        word =  request.form['search']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT MAX(ID) FROM SEARCH ID"""
            cursor.execute(query)
            data = cursor.fetchall()
            counter = int(data[0][0]) + 1

            cursor.execute("INSERT INTO SEARCH(ID, WORD) VALUES ('%d', '%s')"%(counter, word))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ "\n"

    return render_template('search.html', message=message)

@app.route('/update_search', methods=['GET', 'POST'])
def update_search():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id'])
        text = request.form['text']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query=""""""
            cursor.execute("UPDATE SEARCH SET WORD = '%s' WHERE ID = '%d'"%(text, id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ "\n"


    return render_template('update_search.html', message=message)

@app.route('/delete_search', methods=['GET', 'POST'])
def delete_search():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id_del'])
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query=""""""
            cursor.execute("DELETE FROM SEARCH WHERE ID = '%d'"%(id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ "\n"


    return render_template('delete_search.html', message=message)

@app.route('/post', methods=['GET', 'POST'])
def post():
    message=" "

    if request.method == 'POST':
        post_user =  request.form['post_user']
        post_word = request.form['post_word']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT MAX(ID) FROM post_tb ID"""
            cursor.execute(query)
            data = cursor.fetchall()
            counter = int(data[0][0]) + 1

            cursor.execute("INSERT INTO post_tb(ID, SENDER, MESSAGE) VALUES ('%d', '%s','%s')"%(counter, post_user,post_word))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM post_tb"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ " " + row[2]

    return render_template('post.html', message=message)

@app.route('/delete_post', methods=['GET', 'POST'])
def delete_post():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id_post_delete'])
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM post_tb WHERE ID = '%d'"%(id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM post_tb"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ " " + row[2]


    return render_template('delete_post.html', message=message)

@app.route('/update_post', methods=['GET', 'POST'])
def update_post():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id_post_update'])
        text = request.form['new_post_text']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE post_tb SET MESSAGE = '%s' WHERE ID = '%d'"%(text, id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM post_tb"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[1]+ " " + row[2]


    return render_template('update_post.html', message=message)

@app.route('/postTable')
def create_table_for_post():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        query="""DROP TABLE IF EXISTS post_tb"""
        cursor.execute(query)

        query="""CREATE TABLE post_tb(ID INTEGER,SENDER VARCHAR(15),MESSAGE VARCHAR(50))"""
        cursor.execute(query)

        query="""INSERT INTO post_tb(ID, SENDER ,MESSAGE) VALUES (1,'First user','First Post')"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home_page'))

@app.route('/UserDbCreate')
def create_table_for_user():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS user_tb"""
        cursor.execute(query)

        query = """DROP TABLE IF EXISTS social_accounts_tb"""
        cursor.execute(query)

        query="""CREATE TABLE social_accounts_tb(ID SERIAL, facebook VARCHAR(100), twitter VARCHAR(100), instagram VARCHAR(100), PRIMARY KEY (ID))"""
        cursor.execute(query)

        query="""CREATE TABLE user_tb(ID SERIAL,Username VARCHAR(40), Password VARCHAR(10), Firstname VARCHAR(40),Lastname VARCHAR(40), Age int,Gender VARCHAR(10),Email VARCHAR(100), Social_ID INTEGER REFERENCES social_accounts_tb(ID) ON DELETE SET NULL, PRIMARY KEY (ID), UNIQUE(Username))"""
        cursor.execute(query)

        query="""INSERT INTO user_tb(Username, Password) VALUES ('kerim','test')"""
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
@app.route('/addEvent', methods=['GET', 'POST'])
def add_event():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT eventName, eventDate, eventLocation FROM events_tb"""
        cursor.execute(query)
        data = cursor.fetchall()

    error = None
    if request.method == 'POST':

        event_name =  request.form['event_name']
        event_date = request.form['event_date']
        event_location = request.form['event_location']

        with aligramdb.connect(app.config['dsn']) as connection:

            cursor = connection.cursor()
            query="""SELECT MAX(ID) FROM event_tb ID"""
            cursor.execute(query)
            data = cursor.fetchall()
#            counter = str(int(data[0][0]) + 1)
            counter = int(data[0][0]) + 1
            cursor.execute("INSERT INTO event_tb(ID, eventName, eventDate, eventLocation) VALUES ('%d', '%s', '%s', '%s')"%(counter, event_name, event_date, event_location))

            connection.commit()

#            return redirect(url_for('home_page'))

    return render_template('addEvent.html', error=None)

@app.route('/events')
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

    now = datetime.datetime.now()
    return render_template('events.html', session=None, current_time=now.ctime())


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
        #app.config['dsn'] = """user='suxlzcvz' password='Fn5SZ6FkjXt1qTZpq52uSqWfqX90S4yi'
        #                       host='jumbo.db.elephantsql.com' dbname='suxlzcvz'"""
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)



