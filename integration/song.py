class Song:

    _title = None
    _lyric = None
    _url = None

    def __init__(self, title, lyric, url):
        self._title = title
        self._lyric = lyric
        self._url = url