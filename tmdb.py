import requests


API_KEY = '5dc6a2cfc9a56f1485f7615e33f37e4a'
API_ENDPOINT = 'https://api.themoviedb.org/3'
LANG = 'ja-JP'

def search(title):
    """
    return:
      [
        {
          id: int,
          genre_ids: [int],
          title,
          original_title,
          popularity: number,
          ...
        },
        ...
      ],
    """

    """
    {
      page,
      results: [
        {
          id: int,
          genre_ids: [int],
          title,
          original_title,
          popularity: number,
          ...
        },
        ...
      ],
    }
    """
    return requests.get(f'{API_ENDPOINT}/search/movie', dict(api_key=API_KEY, query=title, language=LANG, include_adult=False)).json()['results']

def get_detail(movie_id):
    """
    return:
      {
        genres: [
          id: int,
          name,
        ],
        homepage,
        id: int,
        ...
      }
    """

    return requests.get(f'{API_ENDPOINT}/movie/{movie_id}', dict(api_key=API_KEY, language=LANG)).json()

