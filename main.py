import json

import requests
from bottle import get, run

@get('/theather-recommend.json')
def get_theather_recommend():
    print('get_theather_recommend')
    return json.dumps([
        dict(title="スター・ウォーズ／最後のジェダイ",
             url='http://starwars.disney.co.jp/movie/lastjedi.html',
             genre="SF",
             schedule_start='0',
             schedule_end='0'),
        dict(title=" Ｆａｔｅ／ｓｔａｙ　ｎｉｇｈｔ　Ｈｅａｖｅｎｓ　Ｆｅｅｌ　Ⅰ",
             url='http://www.fate-sn.com/',
             genre="Anime",
             schedule_start='0',
             schedule_end='0'),
    ])

if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
