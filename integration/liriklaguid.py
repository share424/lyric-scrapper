from integration.lyricsite import LyricSite
from integration.song import Song
from bs4 import BeautifulSoup
import requests
import tqdm
import re

class LirikLaguId(LyricSite):

    base_url = "https://www.liriklagu.id/"

    def __init__(self):
        super(LirikLaguId, self).__init__(self.base_url)

    def fetchAllSong(self, start_from_last_page=True):
        response = requests.get(self.base_url)
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        navigation = self.parseNavLink(parsed_html.body)
        last_page = 1
        if start_from_last_page:
            last_page = self.getLastPage()
        for i in tqdm.tqdm(range(last_page, navigation['last']+1)):
            try:
                songs = self.fetchPage(i)
                for song in songs:
                    if (self.isExists(song['url'])):
                        continue
                    info = self.fetchSong(song['url'])
                    s = Song(song['title'], info['lyric'], song['url'])
                    self.save(s, i)
            except:
                pass

    def fetchSong(self, url):
        response = requests.get(url)
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        section = parsed_html.body.find('section', attrs={'class': 'new-content'})
        paragraphs = section.find_all('p')
        lyric = []
        for paragraph in paragraphs:
            if paragraph.find('strong') or paragraph.has_attr('class'):
                continue
            p = paragraph.decode_contents().replace("<br/>", "\n").strip()
            p = self.remove_tags(p)
            lyric.append(p)
        return {
            'lyric': "\n".join(lyric)
        }

    def remove_tags(self, text):
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', text)

    def parseNavLink(self, body):
        pagination = body.find('ul', attrs={'class': 'pagination'})
        pages = pagination.find_all('a')
        current_page = int(pagination.find('li', attrs={'class': 'active'}).find('span').decode_contents().strip())
        last_page = 0
        for page in pages:
            try:
                p = int(page.decode_contents().strip())
                last_page = max(p, last_page)
            except:
                pass
        return {
            'current': current_page,
            'prev': max(1, current_page-1),
            'next': min(last_page, current_page+1),
            'last': last_page
        }

    def fetchPage(self, page):
        response = requests.get(f"{self.base_url}?page={page}")
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        main = parsed_html.body.find('div', attrs={'role': 'main'}).find('div', attrs={'role': 'main'})
        songs = main.find_all('article')
        parsed_song = []
        for song in songs:
            h2 = song.find('h2', attrs={'class': 'entry-title ktz-titlemini'})
            a = h2.find('a')
            parsed_song.append({
                'title': a.decode_contents().strip(),
                'url': a['href']
            })
        return parsed_song