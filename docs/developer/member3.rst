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
