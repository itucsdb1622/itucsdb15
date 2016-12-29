Parts Implemented by Muhammet Berhak DEMİR
================================

Bu projede posts ve iş geçmişi olmak üzere 2 tane varlık geliştirdim. Ayrıca bu varlıklar için aşağıda tanımladığım fonksiyonları 
geliştirdim.



Operasyonlar
------------
* Tablo Oluşturma
 Bu operasyonu tabloları yaratmak için oluşturdum. Bu operasyon sırasında öncelikle eğer tablo varsa drop yapılır. Daha sonra bu
 tablolar istenilen özelliklerle yaratılır.
* Ekleme
 Bu operasyonu yeni tablolarımıza yeni eleman eklemek için kullandım. 
* Silme
 Bu işlem tablolarımızdan artık bulunmasını istemediğimiz elemanları silmek için kullanılıyor.
* Güncelleme
 Bu işlem ise bazı bilgilerini değiştirmek istediğimiz elemanların verilerini değiştirmek için kullanılıyor.

Post Tablosu
-------------
 Bu tablo kullanıcıların yapmış oldukları Postları tutmak için tasarlandı. Primary key ve foreign key post id ve user id olarak tanımlandı. 
 
Tabloyu Oluşturma
^^^^^^^^^^^^^^^^
 Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.

 Python kodu aşağıdaki gibidir:
 
 .. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query="""DROP TABLE IF EXISTS post_tb"""
            cursor.execute(query)

            query="""CREATE TABLE post_tb(ID SERIAL,UserID INTEGER REFERENCES user_tb(ID) ON DELETE SET NULL, MESSAGE VARCHAR(140),     
            PRIMARY KEY (ID))"""
            cursor.execute(query)

Ekleme
^^^^^^^^^^^^^^^^
Bu operasyon Postlara yeni bir kayıt eklemek için kullanılır:

Python kodu aşağıdaki gibidir:

.. code-block:: python
 
 def post():
    message=" "

    if request.method == 'POST':
        post_word = request.form['post_word']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query="""SELECT MAX(ID) FROM post_tb ID"""
            cursor.execute(query)
            data = cursor.fetchall()

            cursor.execute("INSERT INTO post_tb(UserID,MESSAGE) VALUES ('%d','%s')"%(session['loggedUserID'],post_word))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM post_tb"""
        cursor.execute(query)
        data = cursor.fetchall()


    return render_template('post.html', post_list=data)

Güncelleme 
^^^^^^^^^^
Bu işlem daha önceden eklenmiş olan bir Post'un bilgisini değiştirmemizi sağlıyor.

 Python kodu aşağıdaki gibidir.

.. code-block:: python

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

    return render_template('update_post.html',  post_list=data)

Silme 
^^^^^
Bu işlem istenilen bir Post satırının silinmesi için kullanılıyor.

Python kodu aşağıdaki gibidir.

.. code-block:: python

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


    return render_template('delete_post.html',  post_list=data)


İş Tecrübesi Tablosu
---------------
Bu tablo kullanıcıların profil sayfalarında iş tecrübesi bilgilerinin tutulması için tasarlandı. Primary key ve foreign key post id ve user id olarak tanımlandı.

Tabloyu Oluşturma 
^^^^^^^^^^^^^^^^
Bu işlemde öncelikle tablo daha önce var mı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi gerçekleşiyor.

Python kodu aşağıdaki gibidir:

.. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS is_tecrubesi"""
            cursor.execute(query)

            query="""CREATE TABLE is_tecrubesi(ID SERIAL,UserID INTEGER REFERENCES user_tb(ID) ON DELETE SET NULL, isYeri 
            VARCHAR(140),pozisyon VARCHAR(140),sure VARCHAR(140), PRIMARY KEY (ID))"""
            cursor.execute(query)

            
            cursor.execute(query)


Ekleme ve Güncelleme
^^^^^^
Bu operasyon iş tecrübesine yeni bir kayıt eklemek için ve o kullanıcının iş tecrübelerini güncellemesi için kullanılır. 
 
 Python kodu aşağıdaki gibidir:
 
 .. code-block:: python

   def is_tecrubesi_ekle():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if request.method == 'POST':

            sirket = request.form['sirket']
            posizyon = request.form['posizyon']
            sure = request.form['sure']

            cursor.execute("INSERT INTO is_tecrubesi(UserID, isYeri, pozisyon, sure) VALUES ('%d','%s', '%s', '%s')"%
            (session['loggedUserID'],sirket, posizyon, sure))
            return render_template('add_istecrube.html')


    return render_template('add_comment.html', comment_list=data)

Silme
^^^^^
Bu işlem kullanıcının silmek istediği bir iş tecrübesi için kullanılır. İşyeri ismini girerek ilgili iş tecrübesi silinmiş olur.

Python kodu aşağıdaki gibidir:
 
 .. code-block:: python
def is_tecrubesi_islemleri():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        if request.method == 'POST':

            sirket = request.form['sirket']
            cursor.execute("DELETE FROM is_tecrubesi WHERE UserID = '%d' AND isYeri='%s'"%(session['loggedUserID'],sirket))


    return render_template('delete_istecrube.html')



