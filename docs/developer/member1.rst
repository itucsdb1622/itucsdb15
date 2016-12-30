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
