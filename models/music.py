import io
import abc
import csv
import requests
from typing import List

import aubio
import librosa

from utils.spotify_service import SpotifyService
from utils.google_service import GoogleSheetService


class BPMDetector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_bpm(self):
        pass


class LibrosaBPMDetector(BPMDetector):
    def __init__(self, track_id: str):
        self.track_id = track_id

    def get_bpm(self):
        if not self.track_id:
            return 0.0

        preview_url = SpotifyService().get_preview_url(self.track_id)

        response = requests.get(preview_url)
        audio_data = io.BytesIO(response.content)

        y, sr = librosa.load(audio_data)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        return f'{tempo:.2f}'


class AubioBPMDetector(BPMDetector):
    def __init__(self, track_id: str):
        self.track_id = track_id

    def get_bpm(self):
        if not self.track_id:
            return 0.0

        audio_analysis = SpotifyService().get_audio_analysis(self.track_id)
        import json
        with open('audio_analysis.json', 'w') as f:
            f.write(json.dumps(audio_analysis))
        # Get audio data from analysis
        tempo = audio_analysis['track']['tempo']
        audio_data = audio_analysis['segments'][0]['timbre']
        return tempo
        # Calculate BPM using aubio
        # samplerate = 44100
        # hop_size = len(audio_data) // 8
        # print('>>>>>>> hop_size:', hop_size)
        # tempo_detector = aubio.tempo('specdiff', hop_size, samplerate)
        # tempo_detector.set_bpm(tempo)
        # bpm = tempo_detector(audio_data)
        
        # return f'{bpm:.2f}'


def update_to_sheet(track_ds: List[dict], spreadsheet_id: str, sheet_range: str):
    if not track_ds:
        return

    tracks = [list(track_d.values()) for track_d in track_ds]
    GoogleSheetService().upsert_rows(spreadsheet_id, sheet_range, tracks, to_append=True)


def export_csv(filename: str, track_ds: List[dict]):
    headers = ['id', 'name', 'bpm', 'artist', 'duration_ms', 'external_url']

    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')

        writer.writerow(headers)

        for track_d in track_ds:
            writer.writerow([track_d[key] for key in headers])


def read_csv(filename: str) -> List[dict]:
    with open(f'{filename}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')
        headers = next(reader)

        return [dict(zip(headers, row)) for row in reader]


def export_tracks(playlist_id: str):
    track_ds = SpotifyService().get_track_ds(playlist_id)
    export_csv(playlist_id, track_ds)


def get_playlist_and_export_csv(playlist_id: str):
    track_ds = SpotifyService().get_track_ds(playlist_id)
    export_csv(playlist_id, track_ds)


def update_tracks_to_spreadsheet(
    playlist_ids: List[str], spreadsheet_id: str, sheet_range: str
):
    """
    Update Spotify playlists to Google Sheets.
    Args:
        spreadsheet_id: ID of the Google Sheets spreadsheet.
        sheet_range: Range of the sheet to update (e.g. 'Sheet1!A1:B2').
    """

    track_ds = SpotifyService().get_track_ds(playlist_ids)
    tracks = [list(track_d.values()) for track_d in track_ds]
    GoogleSheetService().upsert_rows(spreadsheet_id, sheet_range, tracks, to_append=True)


def update_playlists_to_spreadsheet(spreadsheet_id: str, sheet_range: str):
    """
    Update Spotify playlists to Google Sheets.
    Args:
        spreadsheet_id: ID of the Google Sheets spreadsheet.
        sheet_range: Range of the sheet to update (e.g. 'Sheet1!A1:B2').
    """
    playlist_item_ds = SpotifyService('playlist-read-private').get_all_playlist_items()

    formated_playlist_items = [
        [
            item_d['id'],
            item_d['name'],
            item_d['owner']['display_name'],
            item_d['description'],
            item_d['tracks']['total'],
            item_d['external_urls']['spotify'],
            item_d['tracks']['href'],
            item_d['public'],
        ]
        for item_d in playlist_item_ds
    ]

    GoogleSheetService().upsert_rows(
        spreadsheet_id, sheet_range, formated_playlist_items
    )
