from operator import itemgetter
import json

from bottle import get, run, request

from toho import get_now_playings
from tmdb import search, get_detail

now_playings = None


def prepare():
    global now_playings
    now_playings = get_now_playings()
    with open('now_playings.json', 'wt', encoding='utf-8') as f:
        json.dump(now_playings, f)


@get('/genres.json')
def get_genres():
    titles = [data['name']
              for data in now_playings
              if len(data['schedule']) != 0]
    genres = []
    for title in titles:
        results = search(title)
        if len(results) == 0:
            continue
        movie_id = results[0]['id']
        genres += [e['name'] for e in get_detail(movie_id)['genres']]

    genre_set = {genre for genre in genres}
    genre_rate = []  # type: Tuple[str, int]
    for genre in genre_set:
        genre_rate.append((genre, len([e for e in genres if e == genre])))
    # sort by rate
    genre_rate = sorted(genre_rate, key=itemgetter(1), reverse=True)

    return json.dumps([e[0] for e in genre_rate])


@get('/theather-recommend.json')
def get_theather_recommend():
    """
    return:
      [
        {
          title,
          url,
          schedule_start: date +'%H時%M分'
        },
        ...
      ]
    """

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

    genre = request.query['genre']
    print('get_theather_recommend')

    # TODO schedule
    movies = [dict(title=data['name'],
                   schedule_start=data['schedule'][0]['showingStart'])
              for data in now_playings
              if len(data['schedule']) != 0]

    ret = []
    for movie in movies:
        results = search(movie['title'])
        if len(results) == 0:
            continue
        movie_id = results[0]['id']
        detail = get_detail(movie_id)
        if genre not in [e['name'] for e in detail['genres']]:
            continue
        movie['url'] = detail['homepage']
        ret += movie

    print(ret)
    return json.dumps(ret)


if __name__ == '__main__':
    prepare()
    run(host='0.0.0.0', port=8080)
