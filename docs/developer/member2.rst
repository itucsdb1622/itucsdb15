Parts Implemented by Ali KADAM
================================

Bu projede search, comment ve egitim geçmişi olmak üzere 3 tane varlık geliştirdim. Ayrıca bu varlıklar için aşağıda tanımadığım fonksiyonları geliştirdim.

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
* Arama
 Bu işlemde belirli bir özelliğe göre tablodan elemanları aramamız için kullanılıyor.
 
 Searc Tablosu
 -------------
 Bu tablo kullanıcıların arama geçmişini tutmak için tasarlandı. 
 
 Tabloyu Oluşturma
 ^^^^^^^^^^^^^^^^^
 Bu işlemde öncelikle tablo daha önce varmı diye kontrol ediyor. Eger varsa bu varlığı dropluyorum. Daha sonra create işlemi gerçekleşiyor.
 Bu varlık aşağıdaki kolonları içeriyor.
 * SearchID: Primary key, integer olarak tanımlandı. Satırın id değerini tutuyor.
 * UserID: Foreign Key, integer olarak tanımlandı. Arama yapmış olan kullanıcın id değerini tutmak için tasarlandı.
 * WORD: Varchar olarak tanımlandı. Aranmış kelimeyi tutmak için tasarlandı.
 
 Python kodu aşağıdaki gibidir.









