from integration.lyricsite import LyricSite
from integration.song import Song
from bs4 import BeautifulSoup
import requests
import tqdm

class LirikLaguIndonesiaNet(LyricSite):

    base_url = "https://liriklaguindonesia.net/"

    def __init__(self):
        super(LirikLaguIndonesiaNet, self).__init__(self.base_url)

    def fetchAllSong(self, start_from_last_page=True):
        # fetch all song page
        response = requests.get(self.base_url)
        # get total pages
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        navigation = self.parseNavLink(parsed_html.body)
        last_page = 1
        if start_from_last_page:
            last_page = self.getLastPage()
        for i in tqdm.tqdm(range(last_page, navigation['last']+1)):
            try:
                songs = self.fetchPage(i)
                for song in songs:
                    # skip if exists
                    if(self.isExists(song['url'])):
                        continue
                    info = self.fetchSong(song['url'])
                    s = Song(song['title'], info['lyric'], song['url'])
                    self.save(s, i)
            except:
                pass
            
    def fetchSong(self, url):
        response = requests.get(url)
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        content = parsed_html.body.find('article').find('div', attrs={'style': "background-color:#eee; padding:10px; border-top:2px solid #000; border-bottom:2px solid #000;"})
        paragraphs = content.find_all('p')
        lyric = []
        for paragraph in paragraphs:
            p = paragraph.decode_contents().replace("<br/>", "\n").strip()
            lyric.append(p)
        return {
            'lyric': "\n".join(lyric)
        }


    def parseNavLink(self, body):
        # find nav links
        nav_link = body.find('div', attrs={'class': 'nav-links'})

        # get all pages
        pages = nav_link.find_all('a', attrs={'class': 'page-numbers'})
        current_page = int(nav_link.find('span', attrs={'class': 'page-numbers current'}).decode_contents().strip().replace(",", ""))
        last_page = 0
        for page in pages:
            p = page.decode_contents().strip().replace(",", "")
            try:
                p = int(p)
                last_page = max(p, last_page)
            except:
                continue
        next_page = min(last_page, current_page + 1)
        prev_page = max(1, current_page - 1)
        return {
            'prev': prev_page,
            'current': current_page,
            'next': next_page,
            'last': last_page
        }

    def fetchPage(self, page):
        # fetch page
        response = requests.get(self.base_url + "page/" + str(page))
        parsed_html = BeautifulSoup(response.text, features='html.parser')
        # get all song in this page
        songs = parsed_html.body.find_all('article')
        parsed_song = []
        for song in songs:
            a = song.find('a')
            title = a['title']
            url = a['href']
            parsed_song.append({
                'title': title,
                'url': url
            })

        # fetch nav links
        # navigation = self.parseNavLink(parsed_html.body)
        return parsed_song

    
