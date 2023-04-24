import abc
import io
import requests

import librosa
from spotipy.exceptions import SpotifyException

from utils.spotify_service import SpotifyService


class BPMDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_bpm(self):
        pass


class LibrosaBPMDetector(BPMDetector):
    def __init__(self, track_id: str):
        self.track_id = track_id

    def get_bpm(self) -> str:
        if not self.track_id:
            return '0.0'

        preview_url = SpotifyService().get_preview_url(self.track_id)

        response = requests.get(preview_url)
        audio_data = io.BytesIO(response.content)

        y, sr = librosa.load(audio_data)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return f'{tempo:.2f}'


class SpotifyBPMDetector(BPMDetector):
    def __init__(self, track_id: str):
        self.track_id = track_id

    def get_bpm(self) -> str:
        if not self.track_id:
            return '0.0'

        try:
            audio_analysis = SpotifyService().get_audio_analysis(self.track_id)
            tempo = audio_analysis['track'].get('tempo', 0.0)
            return f'{tempo:.2f}'

        except SpotifyException:
            raise
