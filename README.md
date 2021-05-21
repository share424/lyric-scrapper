# Lyric Scrapper
Lyric Scrapper adalah aplikasi untuk scrapping lirik lagu dari internet

## Installation
Jalankan perintah
```
$ pip install -r requirements.txt
```

## Available Integration
1. [liriklagu.id](https://www.liriklagu.id/)
2. [liriklaguindonesia.net](https://liriklaguindonesia.net/)

## How to use?
Jalankan perintah berikut
```
$ python main.py
```

lalu selanjutnya masukkan nomor situs yang ingin di-scrap.

Hasil scrapping akan disimpan ke dalam file sqlite jika kalian tidak menginstall mongodb.

Jika kalian ingin menggunakan mongodb, atur koneksinya pada file [lyricsite.py](https://github.com/share424/lyric-scrapper/blob/master/integration/lyricsite.py). jangan lupa install mongoclient dengan perintah berikut
```
$ pip install pymongo
```


## Contribution
Kalian bisa melakukan kontribusi untuk integrasi dengan situs lainya dengan mengirimkan pull request

## License
Semua lirik lagu hasil scrapping merupakan hak cipta dari sang penulis lagu tersebut. Aplikasi ini hanya bertujuan untuk scrapping dari situs penyedia lirik lagu. Situs penyedia lirik memiliki hak penuh terhadap integrasi yang ada pada aplikasi ini
