Umut Yazgan Tarafından Eklenen Kısımlar
================================

events_tb, event_pics_tb and event_comments tabloları oluşturuldu. Bu tabloların ekleme, silme, güncelleme metotları eklendi.

events_tb Tablosu
-----------------

events_tb tablosu bütün event'lerin tutulduğu tablodur. Event'i oluşturan kullanıcının bilgisini tutabilmek için user_tb tablosuna bağlantılıdır. Tablo, kullanıcı tarafından herhangi bir bağlantı ile girilemeyen "/DbCreate" yolunda oluşturulmaktadır. Bu yol içerisinde events_tb tablosunu oluşturan kod aşağıda verilmiştir:

.. code-block:: python

    query = """DROP TABLE IF EXISTS events_tb"""
    cursor.execute(query)
    
    # bu arada başka alakasız kod satırları var
    
    query="""CREATE TABLE IF NOT EXISTS events_tb(
                 ID              SERIAL PRIMARY KEY,
                 userID          INTEGER NOT NULL REFERENCES user_tb (ID)
                                 ON DELETE CASCADE ON UPDATE CASCADE,
                 eventName       VARCHAR(50),
                 eventDate       VARCHAR(20),
                 eventLocation   VARCHAR(50))"""

    cursor.execute(query)
    
Event'leri Görüntüleme
^^^^^^^^^^^^^^^^^^^^^^

events sayfasına girildiğinde ilk olarak mevcut event'lerin bir listesi görülür. Bunu gerçeklemek için "show_events()" metodu yazılmıştır.

.. code-block:: python

    @app.route('/events')
    def show_events():
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events_tb"""
            cursor.execute(query)
            events = cursor.fetchall()

            connection.commit()

        now = datetime.datetime.now()
        return render_template('events.html', session=session, current_time=now.ctime(), events=events)

Ayrıca herhangi bir event'in yanındaki "Details" bağlantısı da kullanıcıyı o event'in sayfasına yönlendirir. Burada event'in bütün bilgileri, event ile bağlantılı görseller ve event ile bağlantılı yorumlar görünür. Bu sayfa için de "display_event(event_id)" metodu yazılmıştır.

.. code-block:: python

    @app.route('/events/<event_id>', methods=['GET'])
    def display_event(event_id):

        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT * FROM events_tb WHERE ID = {}""".format(event_id)
            cursor.execute(query)
            event = cursor.fetchone()
            query = """SELECT * FROM event_pics_tb
                           WHERE event_id = %s"""
            data = (event_id,)
            cursor.execute(query, data)
            event_pics = cursor.fetchall()
            query = """SELECT u.username, ec.comment, ec.id FROM event_comments ec
                       JOIN user_tb u ON ec.user_id = u.id
                       WHERE ec.event_id = %s"""
            cursor.execute(query, data)
            event_comments = cursor.fetchall()

        return render_template('manage_event.html', session=session, event=event,
                               event_pics=event_pics, event_comments=event_comments)
                               
Event Ekleme
^^^^^^^^^^^^

Kullanıcı girişi yapmış kişiler events sayfasında "Create Event" butonuna tıklayarak event oluşturabilirler. Oluşturulan event çoklusu events_tb tablosuna eklenir. Bu özelliği gerçeklemek için "add_event()" metodu yazılmıştır.

.. code-block:: python

    @app.route('/addEvent', methods=['GET', 'POST'])
    def add_event():
        if request.method == 'POST':

            event_name =  request.form['event_name']
            event_date = request.form['event_date']
            event_location = request.form['event_location']
            userID = session["loggedUserID"]

            with aligramdb.connect(app.config['dsn']) as connection:

                cursor = connection.cursor()
                cursor.execute("""INSERT INTO events_tb
                                     (userID, eventName, eventDate, eventLocation)
                                  VALUES
                                     (%s, '%s', '%s', '%s')"""
                                %(userID, event_name, event_date, event_location))

                connection.commit()

                    return redirect('events')

        return render_template('addEvent.html', error=None)
        
Event Güncelleme
^^^^^^^^^^^^^^^^

Event'i oluşturan kişi oluşturduğu event'in sayfasında bilgileri tekrar girip "Update" butonuna tıklayarak event'i güncelleyebilir. Sayfadan gönderilen ID'ye sahip çoklu events_tb tablosunda bulunur ve güncellenir. "update_event(event_id)" metodu bu işlevi gerçekleştirmek için yazılmıştır.

.. code-block:: python

    @app.route('/events/<event_id>/update', methods=['POST'])
    def update_event(event_id):

        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            event_name =  request.form['event_name']
            event_date = request.form['event_date']
            event_location = request.form['event_location']

            query = """UPDATE events_tb
                       SET eventname = %s, eventdate = %s, eventlocation = %s
                       WHERE ID = %s"""
            data = (event_name, event_date, event_location, event_id)
            cursor.execute(query, data)

        return redirect('events')

Event Silme
^^^^^^^^^^^

Event'in sayfasında event'i oluşturan kişi "Delete" butonuna tıklayarak event'i tablodan silebilir. Bu işlevi gerçekleştrimek için "delete_event(event_id)" metodu yazılmıştır. Verilen "event_id"ye eşit "ID" değerine sahip olan çoklu events_tb içinden çıkarılır.

.. code-block:: python

    @app.route('/events/<event_id>/delete', methods=['POST'])
    def delete_event(event_id):
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM events_tb WHERE ID = {}""".format(event_id)
            cursor.execute(query)

        return redirect('events')
        
event_pics_tb Tablosu
---------------------

event_pics_tb tablosu event'ler için eklenen görselleri tutar. Görselin kendi "ID"si("ID"), ait olduğu event'in "ID"si("event_id") ve görselin bulunduğu URL("image_url") tablonun sütunlarını oluşturur. "event_id" üzerinden "events_tb" tablosuna bağlıdır. Tablonun oluşturulması için yazılan kod aşağıda verilmiştir:

.. code-block:: python

    query = """DROP TABLE IF EXISTS event_pics_tb"""
    cursor.execute(query)
        
    # bu arada başka alakasız kod satırları var
    
    query = """CREATE TABLE IF NOT EXISTS event_pics_tb(
                   ID           SERIAL PRIMARY KEY,
                   image_url    VARCHAR(256),
                   event_id     INTEGER NOT NULL REFERENCES events_tb (ID)
                                ON DELETE CASCADE ON UPDATE CASCADE)"""
    cursor.execute(query)
    
Event'e Görsel Ekleme
^^^^^^^^^^^^^^^^^^^^^

Bir event'in sayfasındaki "Add Picture" butonuna tıklayan kullanıcı görsel ekleme sayfasına yönlendirilir. Burada yazı kutucuğuna görsel URL'si girip "Add" butonuna tıklayan kişi "event_pics_tb" tablosuna sözü geçen event ile bağlantılı yeni bir çoklu eklemiş olur. Bu işlem "add_picture_to_event(event_id)" metodu ile gerçekleştirilir.

.. code-block:: python

    @app.route('/events/<event_id>/add_picture', methods=['GET', 'POST'])
    def add_picture_to_event(event_id):

        if request.method == 'POST':

            with aligramdb.connect(app.config['dsn']) as connection:
                cursor = connection.cursor()
                image_url = request.form['image_url']
                query = """INSERT INTO event_pics_tb (image_url, event_id)
                               VALUES (%s, %s)"""
                data = (image_url, event_id)
                cursor.execute(query, data)

                return redirect('events/%s' % event_id)

        return render_template('add_picture_to_event.html', event_id=event_id)
        
Görsel Görüntüleme
^^^^^^^^^^^^^^^^^^^

Event'in sayfasında görsele ait küçük resme tıklandığı takdirde görselin sayfasına ulaşılır. Burada görselin daha büyük boyutlu bir hali görülür. Bu işlem "display_image(event_id, image_id)" metodu ile gerçeklenmiştir. Metod tablo içerisinden "event_id" ve "image_id" ile eşleşen "event_id" ve "ID" değişkenlerine sahip çokluyu seçer.

.. code-block:: python

    @app.route('/events/<event_id>/images/<image_id>', methods=['GET'])
    def display_image(event_id, image_id):

        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """SELECT ep.id, ep.image_url, e.userid FROM event_pics_tb ep
                       JOIN events_tb e ON ep.event_id = e.id
                       WHERE ep.id = %s"""
            data = (image_id,)
            cursor.execute(query, data)
            image = cursor.fetchone()

       return render_template('manage_image.html', session=session, image=image,
                               event_id=event_id)
                               
Görsel Güncelleme
^^^^^^^^^^^^^^^^^

Görselin sayfasında event'i açan kişinin görebileceği bir yazı kutucuğu ve bir "Update" butonu mevcuttur. Bu kutucuğa yeni URL girilip "Update"e tıklandığı takdirde mevcut görselin "image_url" alanı girilen yeni URL ile güncellenecektir. "update_image(event_id, image_id)" metodu bu işlem için yazılmıştır.

.. code-block:: python

    @app.route('/events/<event_id>/images/<image_id>/update', methods=['POST'])
    def update_image(event_id, image_id):

        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            image_url =  request.form['image_url']

            query = """UPDATE event_pics_tb
                       SET image_url = %s
                       WHERE ID = %s"""
            data = (image_url, image_id)
            cursor.execute(query, data)

        return redirect('events/%s' % event_id)
        
Görsel Silme
^^^^^^^^^^^^

Görselin sayfasındaki "Delete" butonuna tıklandığı zaman çoklu tablodan çıkarılır. Bu fonksiyon "delete_image(event_id, image_id)" metodunda kodlanmıştır.

.. code-block:: python

    @app.route('/events/<event_id>/images/<image_id>/delete', methods=['POST'])
    def delete_image(event_id, image_id):
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM event_pics_tb WHERE ID = {}""".format(image_id)
            cursor.execute(query)

        return redirect('events/%s' % event_id)
        
event_comments Tablosu
----------------------

event_comments tablosu event'lere kullanıcıların yaptığı yorumları tutar. Hangi yorumun hangi kullanıcı tarafından hangi event'e atıldığının kaydının tutulabilmesi için tablo hem "user_tb" hem de "events_tb" tablolarına bağlıdır. Tablo kendi "ID"sinin yanı sıra sözü edilen tabloların "ID" sütunları ile bağlantı kurabilmek adına sırasıyla "user_id" ve "event_id" sütunlarına sahiptir. Son olarak da asıl verinin mevcut olduğu "comment" sütununa sahiptir. "/DbCreate" içerisinde bulunan tabloyu oluşturan kod ile bu sütunlar daha ayrıntılı görülebilir:

.. code-block:: python

    query = """DROP TABLE IF EXISTS event_comments"""
    cursor.execute(query)
            
    # bu arada başka alakasız kod satırları var
    
    query = """CREATE TABLE event_comments(
                   ID       SERIAL PRIMARY KEY,
                   event_id INTEGER NOT NULL REFERENCES events_tb (ID)
                            ON DELETE CASCADE ON UPDATE CASCADE,
                   user_id  INTEGER NOT NULL REFERENCES user_tb (ID)
                            ON DELETE CASCADE ON UPDATE CASCADE,
                   comment  VARCHAR(256))"""
    cursor.execute(query)
    
Yorum Görüntüleme
^^^^^^^^^^^^^^^^^

Yorumlar ait oldukları event'in sayfasında görünürler. Tablodan doğru event'e ait yorumların çekilip görüntülenmesi işlemi için kullanılan kod daha önce yukarıda event görüntüleme kısmında verilmiştir.

.. code-block:: python

    #   Bu kısımda başka kodlar mevcut
    #
        query = """SELECT u.username, ec.comment, ec.id FROM event_comments ec
                   JOIN user_tb u ON ec.user_id = u.id
                   WHERE ec.event_id = %s"""
        cursor.execute(query, data)
        event_comments = cursor.fetchall()

    return render_template('manage_event.html', session=session, event=event,
                           event_pics=event_pics, event_comments=event_comments)
                           
Yorum Ekleme
^^^^^^^^^^^^

Bir event sayfasında giriş yapmış her kullanıcı yorum atabilir. Atılan yorumların hangi event'e kim tarafından atıldığı bilgisiyle beraber kaydının tutulabilmesi adına "add_comment_to_event(event_id)" metodu yazılmıştır.

.. code-block:: python

    @app.route('/events/<event_id>/comment', methods=['POST'])
    def add_comment_to_event(event_id):
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            comment = request.form['event_comment']
            user_id = session['loggedUserID']
            query = """INSERT INTO event_comments (event_id, user_id, comment)
                           VALUES (%s, %s, %s)"""
            data = (event_id, user_id, comment)
            cursor.execute(query, data)

        return redirect('events/%s' % event_id)
        
Yorum Güncelleme
^^^^^^^^^^^^^^^^

Yorumu atan kullanıcı yorumunun altında bir yazı kutucuğu görecektir. Bu kutucuğa düzeltilmiş yorumunu yazıp "Update" butonuna tıkladığı zaman tabloda o yorumun "comment" kısmı yeni girilen veri ile değiştirilecektir. Bu işlev "update_event_comment(event_id, comment_id)" metodu ile gerçekleştirilir.

.. code-block:: python

    @app.route('/events/<event_id>/comments/<comment_id>/update', methods=['POST'])
    def update_event_comment(event_id, comment_id):

        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            comment = request.form['event_comment']

            query = """UPDATE event_comments
                       SET comment = %s
                       WHERE ID = %s"""
            data = (comment, comment_id)
            cursor.execute(query, data)

        return redirect('events/%s' % event_id)
        
Yorum Silme
^^^^^^^^^^^

Yazılan yorum yazan kişi tarafından yorumun yanındaki "Delete" butonuna tıklanarak silinebilir. Bu işlem o yorumun tutulduğu çokluyu tablodan çıkaracaktır. "delete_event_comment(event_id, comment_id)" metodu bu işlevi yerine getirir.

.. code-block:: python

    @app.route('/events/<event_id>/comments/<comment_id>/delete', methods=['POST'])
    def delete_event_comment(event_id, comment_id):
        with aligramdb.connect(app.config['dsn']) as connection:
            cursor = connection.cursor()
            query = """DELETE FROM event_comments WHERE ID = %s"""
            data = (comment_id,)
            cursor.execute(query, data)

        return redirect('events/%s' % event_id)
