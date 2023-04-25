from typing import List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_USER_ID
from models.multiprocessing import MultiProcessManager


class SpotifyService:
    def __init__(self, scope: str = 'playlist-modify-public'):
        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri='http://www.google.com/',
                scope=scope,
            )
        )

    def get_preview_url(self, track_id: str) -> str:
        return self.spotify.track(track_id)['preview_url']

    def get_audio_analysis(self, track_id: str) -> str:
        return self.spotify.audio_analysis(track_id)

    def get_all_playlist_items(self, item_limit: int = None) -> List[dict]:
        playlists = []
        limit = 50
        offset = 0

        while True:
            result = self.spotify.current_user_playlists(limit=limit, offset=offset)
            playlists.extend(result['items'])
            if not result['next'] or (item_limit and len(playlists) >= item_limit):
                break

            offset += limit

        return playlists[:item_limit] if item_limit else playlists

    def get_item_ds(self, playlist_ids: List[str]) -> List[dict]:
        item_ds = []

        for playlist_id in playlist_ids:
            result = self.spotify.playlist_items(playlist_id)
            item_ds.extend(result['items'])

        return item_ds

    def get_track_ds(self, playlist_ids: List[str]) -> List[dict]:
        formatted_track_ds = []
        item_ds = self.get_item_ds(playlist_ids)

        unique_ids = set()

        unique_item_ds = []

        for item_d in item_ds:
            if 'track' not in item_d or 'id' not in item_d['track']:
                continue

            track_id = item_d['track']['id']
            if track_id and track_id not in unique_ids:
                unique_ids.add(track_id)
                unique_item_ds.append(item_d)

        track_ds = [item_d['track'] for item_d in unique_item_ds]
        formatted_track_ds.extend(MultiProcessManager(8).run(_format_track, track_ds))

        return formatted_track_ds

    def create_playlist(self, name: str, description: str, track_ids: List[str]):
        print(f'>>>>>> Start creating playlist: {name} <<<<<<')
        # create a new playlist
        playlist = self.spotify.user_playlist_create(
            SPOTIFY_USER_ID,
            name,
            description=description,
            public=True,
        )

        # add the tracks to the playlist
        self.spotify.user_playlist_add_tracks(
            self.spotify.current_user()['id'], playlist['id'], track_ids
        )
        print(f'Playlist is created and {len(track_ids)} tracks are added')


def _format_track(track_d: dict):
    from models.music.base import calculate_bpm

    return dict(
        id=track_d['id'],
        name=track_d['name'],
        bpm=calculate_bpm(track_d['id']),
        artist=track_d['artists'][0]['name'],
        duration_ms=track_d['duration_ms'],
        external_url=track_d['external_urls'].get('spotify'),
    )
