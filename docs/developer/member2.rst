Parts Implemented by Ali KADAM
================================

Bu projede search, comment ve egitim geçmişi olmak üzere 3 tane varlık geliştirdim. Ayrıca bu varlıklar için aşağıda tanımadığım fonksiyonları geliştirdim.

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
* Arama
 Bu işlemde belirli bir özelliğe göre tablodan elemanları aramamız için kullanılıyor.
 
Searc Tablosu
-------------
 Bu tablo kullanıcıların arama geçmişini tutmak için tasarlandı. 
 
Tabloyu Oluşturma
^^^^^^^^^^^^^^^^
 Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.
 Bu varlık aşağıdaki kolonları içeriyor.
 * SearchID: 
  Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * UserID: 
  Foreign Key, integer olarak tanımlandı. Arama yapmış olan kullanıcın id değerini tutmak için tasarlandı.
 * WORD: 
  Varchar olarak tanımlandı. Aranmış kelimeyi tutmak için tasarlandı.
 
 Python kodu aşağıdaki gibidir.

.. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS SEARCH"""
            cursor.execute(query)

            query="""CREATE TABLE SEARCH(SearchID SERIAL, UserID INTEGER REFERENCES user_tb(ID) ON DELETE SET NULL, WORD VARCHAR(20),
            PRIMARY KEY (SearchID))"""
            cursor.execute(query)
        
Ekleme 
^^^^^^
Bu operasyon arama geçmişine yeni bir kayıt eklmek için kullanılır. 
 
 Python kodu aşağıdaki gibidir.

.. code-block:: python
 
 def search():
    message=" "

    if request.method == 'POST':
        word =  request.form['search']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO SEARCH(UserID,WORD) VALUES ('%d', '%s')"%(session['loggedUserID'],word))
            connection.commit()

    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            message+=str(row[0])+" "+ row[2]+ "\n"


    return render_template('search.html', search_list=data)
    
Bu aşamda kullanıcıdan html arayüzüyle alınan kelime ve sessindan alınan giriş yapmış kullanıcının idsi kullanılarak ekleme işlemi
yapılır.

Güncelleme 
^^^^^^^^^^
Bu işlem daha önceden eklenmiş olan bir satırın "word" bilgisini değiştirmemizi sağlıyor.

 Python kodu aşağıdaki gibidir.

.. code-block:: python

 def update_search():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id'])
        text = request.form['text']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query=""""""
            cursor.execute("UPDATE SEARCH SET WORD = '%s' WHERE SearchID = '%d'"%(text, id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()

    return render_template('update_search.html', search_list=data)
 
Bu işlem parametrelerini html arayüzüyle kullanıcıdan alıyor.

Silme 
^^^^^
Bu işlem istenilen bir satırın silinmesi için kullanılıyor.

Python kodu aşağıdaki gibidir.

.. code-block:: python

 def delete_search():
    message=" "

    if request.method == 'POST':
        id = int(request.form['id_del'])
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query=""""""
            cursor.execute("DELETE FROM SEARCH WHERE SearchID = '%d'"%(id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM SEARCH"""
        cursor.execute(query)
        data = cursor.fetchall()

    return render_template('delete_search.html', search_list=data)

Bu işlem parametrelerini html arayüzüyle kullanıcıdan alıyor.


Comment Tablosu
---------------
Bu tablo kullanıcıların yapılan postlara yorum yapabilmesi için tasarlandı.

Tabloyu Oluşturma 
^^^^^^^^^^^^^^^^
Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.
Bu varlık aşağıdaki kolonları içeriyor.
 * CommentID: 
  Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * PostID: 
  Foreign Key, integer olarak tanımlandı. Commnet yapılmış olan postun id değerini tutmak için tasarlandı.
 * MESSAGE: 
  Varchar olarak tanımlandı. Yapılmış yorumu tutmak için tasarlandı.
 
Python kodu aşağıdaki gibidir.

.. code-block:: python

    def create_table_for_user():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()

            query = """DROP TABLE IF EXISTS COMMENT"""
            cursor.execute(query)

            query="""CREATE TABLE COMMENT(CommentID SERIAL,PostID INTEGER REFERENCES post_tb(ID) ON DELETE SET NULL, MESSAGE
            VARCHAR(140), PRIMARY KEY (CommentID))"""

            cursor.execute(query)
 
Ekleme 
^^^^^^
Bu operasyon comment tablosuna yeni bir kayıt eklmek için kullanılır. 
 
 Python kodu aşağıdaki gibidir.

.. code-block:: python

 def comment():
    message=" "

    if request.method == 'POST':
        post_id =  request.form['post_id']
        comment = request.form['comment']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO COMMENT(PostID, MESSAGE) VALUES ('%d', '%s')"%(int(post_id), comment))
            connection.commit()

    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM COMMENT"""
        cursor.execute(query)
        data = cursor.fetchall()

    return render_template('add_comment.html', comment_list=data)


Güncelleme 
^^^^^^^^^^
Bu işlem daha önceden eklenmiş olan bir satırın "message" bilgisini değiştirmemizi sağlıyor.

 Python kodu aşağıdaki gibidir.

.. code-block:: python

 def update_comment():

    if request.method == 'POST':
        id = int(request.form['commment_update_id'])
        text = request.form['new_commment_text']
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE COMMENT SET MESSAGE = '%s' WHERE CommentID = '%d'"%(text, id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM COMMENT"""
        cursor.execute(query)
        data = cursor.fetchall()

    return render_template('update_comment.html', comment_list=data)
    
Silme
^^^^^
Bu işlem istenilen bir satırın silinmesi için kullanılıyor.

 Python kodu aşağıdaki gibidir.

.. code-block:: python

 def delete_comment():

    if request.method == 'POST':
        id = int(request.form['comment_delete_id'])
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM COMMENT WHERE CommentID = '%d'"%(id))

            connection.commit()
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query="""SELECT * FROM COMMENT"""
        cursor.execute(query)
        data = cursor.fetchall()


    return render_template('delete_comment.html', comment_list=data)
    
 
Eğitim Geçmişi Tablosu
---------------
Bu tablo kullanıcıların eğitim geçmişini tutmak için tasarlandı.

Tabloyu Oluşturma 
^^^^^^^^^^^^^^^^
Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi
 gerçekleşiyor.
Bu varlık aşağıdaki kolonları içeriyor.
 * ID: 
  Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * UserID: 
  Foreign Key, integer olarak tanımlandı. Bilginin hangi kullanıcıya ait olduğunu anlamak için kullanıcının id değerini tutmak için
  tasarlandı.
 * ilkOkul: 
  Varchar olarak tanımlandı. Kullanıcının ilkokul bilgisini tutmak için tasarlandı.
 * lise: 
  Varchar olarak tanımlandı. Kullanıcının lise bilgisini tutmak için tasarlandı.
 * universite: 
  Varchar olarak tanımlandı. Kullanıcının üniversite bilgisini tutmak için tasarlandı.
 
Python kodu aşağıdaki gibidir.

.. code-block:: python

 def create_table_for_user():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        query = """DROP TABLE IF EXISTS egitim_gecmisi"""
        cursor.execute(query)
        
        query="""CREATE TABLE egitim_gecmisi(ID SERIAL,UserID INTEGER REFERENCES user_tb(ID) ON DELETE SET NULL, ilkOkul
        VARCHAR(140),lise VARCHAR(140),universite VARCHAR(140), PRIMARY KEY (ID))"""
        cursor.execute(query)
        
Ekleme 
^^^^^^
Bu operasyon eğitim geçmişi tablosuna yeni bir kayıt eklmek için kullanılır. social_accounts fonksiyonun içine gerekli kısımlar eklenerek oluşturulmuştur.
 
 Python kodu aşağıdaki gibidir.

.. code-block:: python

 def social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()
        
        ilk_okul=request.form['ilk_okul']
            lise=request.form['lise']
            universite=request.form['universite']

            cursor.execute("SELECT * FROM egitim_gecmisi WHERE UserID = '%d' "%session['loggedUserID'])
            egitim=cursor.fetchall()
            if not egitim:
                cursor.execute("INSERT INTO egitim_gecmisi(UserID, ilkOkul, lise, universite) VALUES ('%d','%s', '%s', '%s')"%
                (session['loggedUserID'],ilk_okul, lise, universite))

            else:
                if ilk_okul:
                    cursor.execute("UPDATE egitim_gecmisi SET ilkOkul='%s'  WHERE UserID='%d' "%(ilk_okul,  session['loggedUserID']))
                if lise:
                    cursor.execute("UPDATE egitim_gecmisi SET  lise='%s' WHERE UserID='%d' "%( lise,  session['loggedUserID']))
                if universite:
                    cursor.execute("UPDATE egitim_gecmisi SET universite='%s' WHERE UserID='%d' "%(universite, session['loggedUserID']))

            return redirect(url_for('profile_page'))
            
Güncelleme 
^^^^^^^^^^
Güncelleme işlemi ekleme fonksiyonuyla iç içe bir yapıda kurulmuştur. Yukarıdaki kodda eğer bu kallnıcının daha önce girilmiş bir 
eğitim geçmişi varsa sadece yeni girilen bilgi kullanılarak (örneğin sadece ilkokul) güncelleme işlemi yapılmaktadır.


Silme
^^^^^
Bu işlem kullanıcının eğitim geçmişinden istenilen verilerin silinmesi için kullanılıyor. Diğer silme işlemlerinden farklı olarak burada bütün satırı silmek istemediğim için silinmek istenilen egitim bilgisinin (örneğin lise) değerini boş string olarak güncelliyorum. 

Python kodu aşağıdaki gibidir. Bu kodda "remove_social_accounts" fonksiyonun içine gömülmüştür.

.. code-block:: python

 def remove_social_accounts():
    with aligramdb.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        if request.method == 'POST':
            ilkOkul = request.form.get('ilkOkulDelete')
            if ilkOkul:
                cursor.execute("UPDATE egitim_gecmisi SET ilkOkul='%s'  WHERE UserID='%d' "%("",  session['loggedUserID']))

            lise = request.form.get('liseDelete')
            if lise:
                cursor.execute("UPDATE egitim_gecmisi SET  lise='%s' WHERE UserID='%d' "%( "",  session['loggedUserID']))

            universite = request.form.get('universiteDelete')
            if universite:
                cursor.execute("UPDATE egitim_gecmisi SET universite='%s' WHERE UserID='%d' "%("", session['loggedUserID']))

     return redirect(url_for('profile_page'))
     
  


