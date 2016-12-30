Parts Implemented by Kerim YILDIRIM
================================

Bu projede kullanıcı, sosyal hesap ve hobi olmak üzere 3 tane varlık geliştirdim. Ayrıca bu varlıklar için aşağıda tanımladığım fonksiyonları geliştirdim.

Operasyonlar
------------
* Tablo Oluşturma
 Bu operasyonu tabloları yaratmak için oluşturdum. Bu operasyon sırasında öncelikle eğer tablo varsa drop yapılır. Daha sonra bu tablolar istenilen özelliklerle yaratılır.
* Ekleme
 Bu operasyonu yeni tablolarımıza yeni eleman eklemek için kullandım. 
* Silme
 Bu işlem tablolarımızdan artık bulunmasını istemediğimiz elemanları silmek için kullanılıyor.
* Güncelleme
 Bu işlem ise bazı bilgilerini değiştirmek istediğimiz elemanların verilerini değiştirmek için kullanılıyor.
* Seçme
 Bu işlemde belirli bir özelliğe göre tablodan elemanları seçmemiz için kullanılıyor.

Kullanıcı tablosu
-------------

Bu tablo kullanıcıların bilgilerini tutmak için tasarlandı. 
 
Tabloyu Oluşturma
^^^^^^^^^^^^^^^^

 Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.
 
 Bu varlık aşağıdaki kolonları içeriyor.
 * ID: 
  Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * Username: 
  Unique ve Varchar olarak tanımlandı. Kullanıcının kullanıcı ismini tutuyor.
 * Password: 
  Varchar olarak tanımlandı. Kullanıcının şifresini tutuyor.
 * Firstname: 
  Varchar olarak tanımlandı. Kullanıcının ismini tutuyor.
 * Lastname: 
  Varchar olarak tanımlandı. Kullanıcının soyismini tutuyor.
 * Age: 
  Integer olarak tanımlandı. Kullanıcının yaşını tutuyor.
 * Gender: 
  Varchar olarak tanımlandı. Kullanıcının cinsiyetini tutuyor.
 * Email: 
  Varchar olarak tanımlandı. Kullanıcının email adresini tutuyor.
 * Social_ID: 
  Foreign key, integer olarak tanımlandı. Kullanıcının sosyal hesap kaydının id'sini tutuyor.
  Kullanıcının sosyal hesap kaydı silinirse bu alan NULL yapılıyor.
 * Hobby_ID: 
  Foreign key, integer olarak tanımlandı. Kullanıcının sosyal hesap kaydının id'sini tutuyor.
  Kullanıcının hobi kaydı silinirse bu alan NULL yapılıyor.
 

 
 Python kodu aşağıdaki gibidir.

.. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS user_tb CASCADE"""
            cursor.execute(query)

            
            query="""CREATE TABLE user_tb(ID SERIAL,Username VARCHAR(40), Password VARCHAR(10), Firstname VARCHAR(40),Lastname                      VARCHAR(40), Age int,Gender VARCHAR(10),Email VARCHAR(100), Social_ID INTEGER REFERENCES                                      social_accounts_tb(ID) ON DELETE SET NULL, Hobby_ID INTEGER REFERENCES hobbies_tb(ID) ON DELETE SET NULL,                      PRIMARY KEY (ID), UNIQUE(Username))"""
            
            cursor.execute(query)


Ekleme 
^^^^^^
Bu operasyon yeni bir kullanıcı kaydı eklemek için kullanılır. 
 
 Python kodu aşağıdaki gibidir.

.. code-block:: python
 
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
    
Bu aşamada kullanıcıdan html arayüzüyle alınan kullanıcı bilgileri ile bir kullanıcı kaydı oluşturulur.


Güncelleme 
^^^^^^^^^^
Bu işlem kayıtlı olan bir kullanıcının kullanıcı ismini güncellememizi sağlıyor.

 Python kodu aşağıdaki gibidir.

.. code-block:: python

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

Silme 
^^^^^
Bu işlem istenilen bir kullanıcı kaydının silinmesi için kullanılıyor.

Python kodu aşağıdaki gibidir.

.. code-block:: python

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

Bu işlem silinecek hesabın id'sini session bilgisinden alıyor.


Sosyal hesap tablosu
-------------

Bu tablo kullanıcıların bilgilerini tutmak için tasarlandı. 
 
Tabloyu Oluşturma
^^^^^^^^^^^^^^^^

 Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.
 
 Bu varlık aşağıdaki kolonları içeriyor.
 * ID: 
  Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * facebook: 
  Varchar olarak tanımlandı. Kullanıcının facebook hesap bilgisini tutuyor.
 * twitter: 
  Varchar olarak tanımlandı. Kullanıcının twitter hesap bilgisini tutuyor.
 * instagram: 
  Varchar olarak tanımlandı. Kullanıcının instagram hesap bilgisini tutuyor.

 

 
 Python kodu aşağıdaki gibidir.

.. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS social_accounts_tb"""
            cursor.execute(query)

            
            query=query="""CREATE TABLE social_accounts_tb(ID SERIAL, facebook VARCHAR(100), twitter VARCHAR(100), instagram                              VARCHAR(100), PRIMARY KEY (ID))"""
            
            cursor.execute(query)
            
            
Ekleme 
^^^^^^
Bu operasyon kullanıcının sosyal medya hesap kaydını eklemek için kullanılır. 

Güncelleme 
^^^^^^^^^^
Bu operasyon kullanıcının sosyal medya hesap bilgilerini güncellemek için kullanılır.
 
 Ekleme ve Güncelleme işlemlerini yapan Python kodu aşağıdaki gibidir.

.. code-block:: python
 
 def social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        cursor.execute("SELECT Social_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
        data_social = cursor.fetchall()

        cursor.execute("SELECT Hobby_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
        data_hobby = cursor.fetchall()

        facebook = ''
        twitter = ''
        instagram = ''

        guitar = False
        basketball = False
        football = False

        if len(data_social) > 0 :

            social_id = data_social[0][0]

            if social_id != None :

                print("social_id", data_social)
                cursor.execute("SELECT facebook, twitter, instagram FROM social_accounts_tb WHERE Id = '%d' "%social_id)
                social_accs = cursor.fetchall()

                facebook = social_accs[0][0]
                twitter = social_accs[0][1]
                instagram = social_accs[0][2]

        if len(data_hobby) > 0 :

            hobby_id = data_hobby[0][0]

            if hobby_id != None :

                cursor.execute("SELECT guitar, basketball, football FROM hobbies_tb WHERE Id = '%d' "%hobby_id)
                hobbies = cursor.fetchall()

                guitar = hobbies[0][0]
                basketball = hobbies[0][1]
                football = hobbies[0][2]






        error = None
        if request.method == 'POST':

            facebook_acc = request.form['facebook account']
            twitter_acc = request.form['twitter account']
            instagram_acc = request.form['instagram account']

            hobby_guitar = request.form['guitar']
            hobby_basketball = request.form['basketball']
            hobby_football = request.form['football']

            hobby_guitar = not bool(hobby_guitar)
            hobby_basketball = not bool(hobby_basketball)
            hobby_football = not bool(hobby_football)


            data = data_social

            if len(data) > 0:
                if data[0][0] == None:
                    cursor.execute("INSERT INTO social_accounts_tb(facebook, twitter, instagram) VALUES ('%s', '%s', '%s') RETURNING id"%(facebook_acc, twitter_acc, instagram_acc))

                    cursor.execute("SELECT lastval()")
                    social_id = cursor.fetchall()
                    social_id = social_id[0][0]

                    cursor.execute("UPDATE user_tb SET Social_ID = '%d' WHERE Username = '%s' "%(social_id, session['loggedUser']))

                else:
                    cursor.execute("UPDATE social_accounts_tb SET facebook ='%s', twitter = '%s', instagram = '%s' WHERE ID='%s' "%(facebook_acc, twitter_acc, instagram_acc, data[0][0]))


            data = data_hobby

            if len(data) > 0:
                if data[0][0] == None:

                    cursor.execute("INSERT INTO hobbies_tb(guitar, basketball, football) VALUES (%s, %s, %s) RETURNING id"%(hobby_guitar, hobby_basketball, hobby_football))

                    cursor.execute("SELECT lastval()")
                    hobby_id = cursor.fetchall()
                    hobby_id = hobby_id[0][0]

                    cursor.execute("UPDATE user_tb SET Hobby_ID = '%d' WHERE Username = '%s' "%(hobby_id, session['loggedUser']))

                else:

                    cursor.execute("UPDATE hobbies_tb SET guitar ='%s', basketball = '%s', football = '%s' WHERE ID='%s' "%(hobby_guitar, hobby_basketball, hobby_football, data[0][0]))



            ilk_okul=request.form['ilk_okul']
            lise=request.form['lise']
            universite=request.form['universite']

            cursor.execute("SELECT * FROM egitim_gecmisi WHERE UserID = '%d' "%session['loggedUserID'])
            egitim=cursor.fetchall()
            if not egitim:
                cursor.execute("INSERT INTO egitim_gecmisi(UserID, ilkOkul, lise, universite) VALUES ('%d','%s', '%s', '%s')"%(session['loggedUserID'],ilk_okul, lise, universite))

            else:
                if ilk_okul:
                    cursor.execute("UPDATE egitim_gecmisi SET ilkOkul='%s'  WHERE UserID='%d' "%(ilk_okul,  session['loggedUserID']))
                if lise:
                    cursor.execute("UPDATE egitim_gecmisi SET  lise='%s' WHERE UserID='%d' "%( lise,        session['loggedUserID']))
                if universite:
                    cursor.execute("UPDATE egitim_gecmisi SET universite='%s' WHERE UserID='%d' "%(universite, session['loggedUserID']))

            return redirect(url_for('profile_page'))
    now = datetime.datetime.now()
    return render_template('social_accounts.html', facebook = facebook, twitter = twitter, instagram = instagram, guitar = guitar, basketball = basketball, football = football, current_time=now.ctime())

        else:

            with aligramdb.connect(app.config['dsn']) as connection:

                cursor = connection.cursor()

                cursor.execute("INSERT INTO user_tb(Username, Password) VALUES ('%s', '%s')"%(username, password))

                connection.commit()

                return redirect(url_for('home_page'))

    return render_template('register.html', error=error)
    
Bu aşamada kullanıcıdan html arayüzüyle alınan sosyal medya hesap bilgileri ile bir kayıt oluşturulur.


Silme 
^^^^^
Bu işlem kullanıcının sosyal medya kaydının silinmesi için kullanılıyor.

Python kodu aşağıdaki gibidir.

.. code-block:: python

 def remove_social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        if request.method == 'POST':

            if not bool(request.form['social']) == True or not bool(request.form['hobby']) == True:
                if not bool(request.form['social']) == True :

                    cursor.execute("SELECT Social_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
                    data = cursor.fetchall()
                    if len(data) > 0:
                        if data[0][0] != None:
                            cursor.execute("DELETE FROM social_accounts_tb WHERE ID = '%d' "%int(data[0][0]))

                    ilkOkul = request.form.get('ilkOkulDelete')
                    if ilkOkul:
                        cursor.execute("UPDATE egitim_gecmisi SET ilkOkul='%s'  WHERE UserID='%d' "%("",  session['loggedUserID']))

                    lise = request.form.get('liseDelete')
                    if lise:
                        cursor.execute("UPDATE egitim_gecmisi SET  lise='%s' WHERE UserID='%d' "%( "",  session['loggedUserID']))

                    universite = request.form.get('universiteDelete')
                    if universite:
                        cursor.execute("UPDATE egitim_gecmisi SET universite='%s' WHERE UserID='%d' "%("", session['loggedUserID']))


                if not bool(request.form['hobby']) == True :

                    cursor.execute("SELECT Hobby_ID FROM user_tb WHERE Username = '%s' "%session['loggedUser'])
                    data = cursor.fetchall()

                    if len(data) > 0:

                        if data[0][0] != None:
                            cursor.execute("DELETE FROM hobbies_tb WHERE ID = '%d' "%int(data[0][0]))


                return redirect(url_for('profile_page'))
            else :

                return redirect(url_for('profile_page'))

    now = datetime.datetime.now()
    return render_template('remove_social_accounts.html', current_time=now.ctime())

