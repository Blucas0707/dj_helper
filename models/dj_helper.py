import random
from typing import List

from models import music as music_m


class DJHelper:
    @staticmethod
    def update_items_to_sheet(
        playlists: List[str], spreadsheet_id: str, sheet_range: str = 'All'
    ):
        song_ds = []
        for playlist in playlists:
            song_ds.append(music_m.get_track_ds(playlist))

        music_m.update_to_sheet(song_ds, spreadsheet_id, sheet_range)


def gen_target_bpms(peaks: List, step: float) -> List:
    flows = []
    for i in range(len(peaks) - 1):
        start = peaks[i]
        end = peaks[i + 1]
        diff = end - start
        if diff <= step:
            flows.append(start)
        else:
            num_segments = diff // step
            segment_size = diff / num_segments
            for j in range(num_segments):
                flows.append(start + j * segment_size)
    flows.append(peaks[-1])

    return flows


def is_bpm_in_tolerance(bpm: float, target_bpm: float, tolerance: float) -> bool:
    return target_bpm - tolerance <= bpm < target_bpm + tolerance


def transform_to_min(duration_ms: float) -> float:
    return duration_ms / 1000 / 60


def get_order_track_ds(
    track_ds: List[dict],
    target_bpms: List[float],
    bpm_tolerance: float = 3.0,
    max_duration_min: float = None,
    max_track_duration_min: float = 5.0,
    to_shuffle: bool = False,
) -> List[dict]:
    duration_min = 0
    playlist_ds = []

    if to_shuffle:
        random.shuffle(track_ds)

    for target_bpm in target_bpms:
        for track_d in track_ds:
            if track_d not in playlist_ds and is_bpm_in_tolerance(
                float(track_d['bpm']), target_bpm, bpm_tolerance
            ):
                track_duration_min = transform_to_min(float(track_d['duration_ms']))
                if track_duration_min > max_track_duration_min:
                    continue

                playlist_ds.append(track_d)
                duration_min += track_duration_min
                break

        if max_duration_min and max_duration_min < duration_min:
            break

    return playlist_ds
