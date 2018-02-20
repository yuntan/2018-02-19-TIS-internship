from time import time
from datetime import datetime
from functools import reduce

import requests

def concat(l):
    return reduce(lambda acc, elem: acc + elem, l)

def concat_safe(l):
    return [x for x in reduce(lambda acc, elem: acc + elem, l) if len(x) != 0]


def get_now_playings():
    """
    movie data and today's schedule
    return:
      [
        {
          name,
          mcode,
          schedule: [
            {
              showingStart: date +%H:%M,
              showingEnd: date +%H:%M,
              ...
            },
            ...
          ],
          ...
        },
        ...
      ]
    """

    # undocumented API for now playing
    # parameters:
    #   _dc: unix time
    # return:
    #   {
    #     data: [
    #       { name, mcode, ... },
    #       ...
    #     ],
    #     status,
    #   }
    NOW_PLAYING_URL = 'https://hlo.tohotheater.jp/data_net/json/movie/TNPI3090.JSON'

    # undocumented API for schedule
    # parameters:
    #   __type__=json
    #   movie_cd: movie code
    #   vg_cd: theather code
    #   show_day: date +%Y%m%d
    #   term=99
    #   _dc: unix time
    # return:
    #   {
    #     status: int,
    #     data: list of movie (normal, dolby, etc) [
    #       {
    #         code,
    #         name: movie title,
    #         ename: english title,
    #         mcode: movie code,
    #         list: list of theather [
    #           {
    #             name: theather name,
    #             list: [
    #               {
    #                 date: date +%Y%m%d,
    #                 list: list of screen [
    #                   {
    #                     name: name of screen
    #                     list: list of schedule [
    #                       {
    #                         showingStart: date +%H:%M,
    #                         showingEnd: date +%H:%M,
    #                         ...
    #                       },
    #                       ...
    #                     ],
    #                     ...
    #                   },
    #                   ...
    #                 ],
    #                 ...
    #               },
    #               ...
    #             ],
    #             ...
    #           },
    #           ...
    #         ],
    #         ...
    #       },
    #       ...
    #     ],
    #   }
    SCHEDULE_URL = 'https://hlo.tohotheater.jp/net/schedule/TNPI3070J01.do'

    # theather code of TOHOシネマズ梅田
    THEATHER_CODE_UMEDA = '037'

    epoch = int(time())
    day = datetime.now().strftime('%Y%m%d')

    movie_data = requests.get(NOW_PLAYING_URL, dict(_dc=epoch)).json()['data']

    for item in movie_data:
        # get today's schedule
        movies = requests.get(SCHEDULE_URL,
                              dict(__type__='json',
                                   movie_cd=item['mcode'],
                                   vg_cd=THEATHER_CODE_UMEDA,
                                   show_day=day,
                                   term=99,
                                   _dc=epoch)).json()['data']
        # # four level nested list
        # item['schedule'] = concat(concat_safe([x for x in concat_safe(
        #     [[[[schedule
        #         for schedule in screen['list']]
        #        for screen in theather['list'][0]['list'] if len(screen['list']) != 0]
        #       for theather in movie.get('list') if len(theather['list']) != 0]
        #      for movie in movies if movie.get('list') and len(movie['list']) != 0]
        # ) if len(x)]))
        schedules = []
        for movie in movies:
            if not movie.get('list'):
                continue
            for theater in movie['list']:
                for screen in theater['list'][0]['list']:
                    for schedule in screen['list']:
                        schedules.append(schedule)

        item['schedule'] = schedules

    return movie_data
