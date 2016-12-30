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
    
Event'leri Gösterme
^^^^^^^^^^^^^^^^^^^

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
    
    
