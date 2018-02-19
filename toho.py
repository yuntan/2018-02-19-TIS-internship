import requests
import lxml.html

def get_now_playing():
    URL = 'https://hlo.tohotheater.jp/net/movie/TNPI3090J01.do'

    html = requests.get(URL).text
    root = lxml.html.fromstring(html)
    return [e.text_content() for e in root.cssselect('.movies .movies-item h2.movies-title')]
