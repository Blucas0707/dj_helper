import click

from settings import SPOTIFY_ALL_PLAYLIST_SPREADSHEET_ID
from models.spotify_service import SpotifyService
from models.music import base as music_m


# fmt: off
CONFIG_D = {
    'blues': {
        'spread_sheet_id': '1YrL6UVXXUChtqf4HdgfKU1nnzPX1SX_KsxaW3-Wf33w',
        'playlist_ids': {'5YBEfrHKAWe2rgYDXAHfnB', '3O8Dd4CObbA8TC1WUTnIbC', '5OaCQ4XinbGtR6TbZfcHcu', '12xzebzBuJJOMrI9hbqHyM', '2JRsFEZNOT9n2UQjSos8Ao', '2CIJJ5ZukQ5iRhpWwhHuDZ', '1nxCCM3Xv3hZhMJ5eCQD06', '5AaJyTsSB1fgsOquaFekZm', '46zo5YiHBhCfUuhWQLxe2R', '1NMnPohYbttFELPf52rlnN', '2RJ8jJ1xbWaPEOcqzpSFWB', '6atnPmXeJnTOwKCAr96pFt', '6PG9OLPdUuavohyTDJddeA', '1phvUuZvEqXhu8WE7MaEFK', '5zqfbSU5i2cu0dicNs8SpU', '2lx0k1fewonWUZuio3ySan', '6fvMzYCz50o7gZ1BrNGU0g', '7F7LtxTGFZeQc519EXM3Fz', '1M6yLkfVryssdEXWxE1cYU', '5Lb3trabd1NEinVk8UQerj', '5WwsvgQRNKeV1AP2ESU3BM', '0D7hUk29y7NAiildT1d8jW', '2H05ducHR1JFjfFzd8Ci7y', '6EtdGxidyHotHoeKlLbYn4', '2xN8XHOVaaIzlxr3WO7dxo', '5xRr6JVdg8QXYIysbvgZtN', '0ax5HgHyWEcXMIoIBdJ6HL', '5pTeTvV6mng8vY4ynbuF2B', '7f714xHeYc0JPmy0fFfpeq', '6ZqU5LadaCEP1HtsprwaFd', '0i55egdiE0esZmomIk1wUL', '3SqBOIAbTNYcxJkPXRLRTB', '6n8BOVL7UPRDOCG8b8AQ5C', '2Vwiw2P1X5iz7npG5o4Q4r', '31PUVY8xshK0anmS0QZlpX', '4Z1tFqLM0QTrLPBwU0GaUY', '4SFClR0bGz9xzeO2LPHHpI', '6SLaRr5A47e0xV5ryEiPyU', '0lJDJ38Mw2TfuUURmjE5OD', '6PTDxFk4LmDNZjB3ZTVmGE', '3Hhn4g871xkqk80s77cmMy', '37i9dQZF1DXcc6f6HRuPnq', '5feyfTNB4G9DX7YY18yXIh', '0qFKkxFDYrZVnTC10nn9U4', '37i9dQZF1DWULaRXVqGMUt', '2hCgbDmQ3PcDuBlg98kRCH', '1xL4C6h7kM2x80OZEWpnOD', '68IVtAILkqevon0U3ajQNX', '14p1Fr2GjRzOjYi5K2StBZ', '0cznH05Fs4ZjH5DYT2HaQW', '26lao4thh1peAzKViwFBH8', '7M4vQi7trxZkBUv7eH0fOk', '2ZsIYBYJDCK2Or3EcfWHlm', '6QYZCWD8JRKMODNjK31WYc', '1Ryn2YHEe62hAxO56pLpuD', '1BpuIdCwQcb5EpZUI3HExU', '1h8VZAl4DMPDPZFVMvbaCt', '1LcCePwGpFxjGNS4LmXk6A', '7mA7Ybhoj3R2XbbOUPFBlO', '7FW0IAVYoT0TuNdtEBlKIu', '3JHLOos6AgjW7XD6c73mYa', '0OXJXzSgGqVB41OnQurrLW', '66jZOrpPSQjdxMNaebIjW5', '1ODVcUT9ZUUTLe0CFcXNcX', '2J4alrQQFeqvanDyckHhG7', '7EI3IVMfebDuKJ72fWMfap', '37i9dQZF1DWSTHVqvNCwNq', '1kjQa69O4cfsGElRvGUHDb', '3I5phWeVZoLu0SjgdN3WiI', '42zklis5t3lXZ6q25Omd3j', '37i9dQZF1DXbkKnGZHv1kf', '3CbFUe8QliW527pQR4iODt', '04RSm7MR5jUNm15tw64iH2', '1ujbpSvTcdW6PXVisv9TMf', '4b7RW7wKYvCrrvsI6lexs1', '5ydK5Lt2AVVDw0oSfIwrow', '2c5WYGIu2vi76WLtjtB0EJ', '3d5EvaD7MgDXHp2aDnN5Yq', '1UoObyFVkL3qFNsROuZV2b', '0Vg6D13LJd2FKlZAbh6O6r', '0qhyc4evtEoCnbw8WJDkct', '5buvee7l1dbINx5lQwcksi', '7Lb4aWDhskQYTElbF5Doxr', '53gwSYUb7teuTy7BWhifw7', '46YEeBQ8KNfSfdU5cVBo1L', '1lg8HTVMhiEcfiAr3h4EiK', '37i9dQZF1DX7nt6DdNdydo', '7qJXtW4COsde0dQXzm4HI8', '4l48zTWzdnw5uT6Zr0WKTa',},
    },
    'balboa': {
        'spread_sheet_id': '1VfRZ8nxUxTip_qfnz7pG__6xtxXhBVDahYZ5DSeb80g',
        'playlist_ids': {'5YBEfrHKAWe2rgYDXAHfnB', '3O8Dd4CObbA8TC1WUTnIbC', '2eiEguPccOnFpUx2AhWJyC', '7GnULBKb0qBfWlIwjrcNhH', '3lzu8F4Ahm0EM45RmYMuiX', '0fMUBlmzWd7DRUOlsq0Wuo', '0iZ7fisFJw28iQ6lDfdI2K', '0S66j7w2lNlkTYAhg2G25U', '1oNMS0XrTtgQwGCmiDdX9J', '7GxIH2wgY4Lk2JZlOIpoc7', '7valA1ft5GaFo4uOI0an8z', '0D7hUk29y7NAiildT1d8jW', '3A68uJvHo3oUnlu6QASHwD', '56Bup4RnMyWoqviNNigyOQ', '4yF3ktRNbzS3J8hXGAW8Lt', '5HjMfQnnMZ4n3PQTdMyN51', '0Ic5MxOkXWQD5sHkDS5q9l', '1I17Oxv9yZSkSnEGwhvqQK', '3CZ0smAQeq7pi1oX0qMYRY', '1LcCePwGpFxjGNS4LmXk6A', '1QpZX4ASwrThTeD6wnBeo5', '6mRBXQW6DWflCIu03GNT4n', '3I5phWeVZoLu0SjgdN3WiI', '1JQ0KjRt89gy0BquY5WEWz', '4izFE6UhsUJhMhx2kLGkfY', '0fcYVtGB0rdOUL5OfUUAcE', '7t7FUvfqS8okdBrnstwrZD', '3hNbMKZPkAzM01gr6itQhh', '1aIzbh3eFJCqfqqdrfQZDA', '4l48zTWzdnw5uT6Zr0WKTa',},
    },
}
# fmt: on


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    '-t',
    '--type',
    'type_',
    required=True,
    type=str,
    help='choose a type to update: playlist, blues, balboa',
)
def update_sheet(type_: str):
    match type_:
        case 'playlist':
            music_m.update_playlists_to_spreadsheet(
                spreadsheet_id=SPOTIFY_ALL_PLAYLIST_SPREADSHEET_ID,
                sheet_range='Playlist!A2',
            )
        case _:
            if type_ not in CONFIG_D:
                return

            spread_sheet_id = CONFIG_D[type_]['spread_sheet_id']
            playlist_ids = CONFIG_D[type_]['playlist_ids']

            music_m.update_tracks_to_spreadsheet(
                playlist_ids=playlist_ids,
                spreadsheet_id=spread_sheet_id,
                sheet_range='All!A2',
            )


@cli.command()
@click.option(
    '-s',
    '--spreadsheet',
    'spreadsheet_id',
    required=True,
    type=str,
    help='Google sheet id',
)
@click.option(
    '-p',
    '--playlist',
    'playlist_id',
    required=True,
    type=str,
    help='Spotify playlist id',
)
@click.option(
    '-r',
    '--range',
    required=True,
    type=str,
    help='range in Google sheet to update',
)
def update_tracks_to_spreadsheet(spreadsheet_id: str, playlist_id: str, range: str):
    """
    Updates the specified range in the Google sheet with the tracks in the specified Spotify playlist.
    """
    music_m.update_tracks_to_spreadsheet(
        [playlist_id], spreadsheet_id, range, with_headers=True
    )
    

@cli.command()
@click.option(
    '-n',
    '--name',
    required=True,
    type=str,
    help='Spotify playlist name',
)
@click.option(
    '-d',
    '--description',
    required=True,
    type=str,
    help='Spotify playlist description',
)
@click.option(
    '-tds',
    '--track_ids',
    required=True,
    type=str,
    help='track ids, ex: a,b,c',
)
def create_playlist(name: str, description: str, track_ids: str):
    """
    Creates a new Spotify playlist with the specified name and description,
    and adds the tracks with the specified ids to the playlist.
    """
    track_ids = track_ids.split(',')
    SpotifyService().create_playlist(name, description, track_ids)


if __name__ == '__main__':
    cli()
