from typing import List

from spotipy.exceptions import SpotifyException

from schema.music.enums import BPMDetecterEnum
from models.google_service import GoogleSheetService
from models.spotify_service import SpotifyService
from models.file import export_csv
from models.music.bpm_detector import LibrosaBPMDetector, SpotifyBPMDetector


HEADERS = [
    'id',
    'name',
    'bpm',
    'artist',
    'duration_ms',
    'external_url',
]

BPM_DETECTOR_TYPE_MAP = {
    BPMDetecterEnum.LISBROSA.value: LibrosaBPMDetector,
    BPMDetecterEnum.SPOTIFY.value: SpotifyBPMDetector,
}


def update_to_sheet(track_ds: List[dict], spreadsheet_id: str, sheet_range: str):
    if not track_ds:
        return

    tracks = [list(track_d.values()) for track_d in track_ds]
    GoogleSheetService().upsert_rows(
        spreadsheet_id, sheet_range, tracks, to_append=True
    )


def export_tracks(playlist_id: str):
    track_ds = SpotifyService().get_track_ds(playlist_id)
    export_csv(HEADERS, playlist_id, track_ds)


def get_playlist_and_export_csv(playlist_id: str):
    track_ds = SpotifyService().get_track_ds(playlist_id)
    export_csv(HEADERS, playlist_id, track_ds)


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
    print(f'Already get {len(track_ds)} tracks from {len(playlist_ids)} playlists')

    tracks = [list(track_d.values()) for track_d in track_ds]
    GoogleSheetService().upsert_rows(
        spreadsheet_id, sheet_range, tracks, to_append=True
    )


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


def calculate_bpm(
    track_id: str, bpm_detecter_type: BPMDetecterEnum = BPMDetecterEnum.SPOTIFY
) -> str:
    bpm = '0.0'

    if not track_id:
        return bpm

    if not (bpm_detecter := BPM_DETECTOR_TYPE_MAP.get(bpm_detecter_type.value)):
        return bpm

    try:
        bpm = bpm_detecter(track_id).get_bpm()
    except SpotifyException:
        bpm = LibrosaBPMDetector(track_id).get_bpm()

    return bpm
