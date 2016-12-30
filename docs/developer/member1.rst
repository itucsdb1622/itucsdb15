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
