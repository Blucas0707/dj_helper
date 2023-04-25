import requests
from enum import Enum

from bs4 import BeautifulSoup

from utils.html import make_query_string


BASE_URL = 'https://jog.fm/'
BPM_GAP = 5


class CategoryEnum(Enum):
    BLUES = 'blues-workout-songs'


def crawl_song_d(
    category: CategoryEnum,
    min_bpm: int,
    max_bpm: int,
    sort_by: str = 'bpm',
    order_by: str = 'asc',
) -> dict:
    if not category:
        raise ValueError('No category specified')

    song_d = {}

    while min_bpm < max_bpm:

        url = make_query_string(
            f'{BASE_URL}{category}',
            {'bpm': min_bpm, 'sort': sort_by, 'order': order_by},
        )

        resp = requests.get(url)

        if resp.status_code != 200:
            raise ValueError('Respsonse is not valid.')

        soup = BeautifulSoup(resp.content, 'html.parser')

        song_items = soup.find_all('div', 'song list-item')

        for song_item in song_items:

            spotify_song = song_item.find('a', 'spotify-song')
            if not spotify_song:
                continue

            if not (
                spotify_uri := song_item.find('a', 'spotify-song').get(
                    'data-spotify-uri'
                )
            ):
                continue

            track_id = spotify_uri.split('spotify:track:')[1]
            bpm = song_item.find('div', 'middle').a.text

            song_d[track_id] = bpm

        min_bpm += BPM_GAP

    return song_d
