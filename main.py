import click

from settings import SPOTIFY_ALL_PLAYLIST_SPREADSHEET_ID
from models import music as music_m
from models.dj_helper import DJHelper
from utils.spotify_service import SpotifyService

# fmt: off
CONFIG_D = {
    'blues': {
        'spread_sheet_id': '1YrL6UVXXUChtqf4HdgfKU1nnzPX1SX_KsxaW3-Wf33w',
        'playlist_ids': ['4SFClR0bGz9xzeO2LPHHpI', '4Z1tFqLM0QTrLPBwU0GaUY', '6SLaRr5A47e0xV5ryEiPyU', '0i55egdiE0esZmomIk1wUL', '3SqBOIAbTNYcxJkPXRLRTB', '6ZqU5LadaCEP1HtsprwaFd', '6n8BOVL7UPRDOCG8b8AQ5C', '0lJDJ38Mw2TfuUURmjE5OD', '2Vwiw2P1X5iz7npG5o4Q4r', '31PUVY8xshK0anmS0QZlpX', '0D7hUk29y7NAiildT1d8jW', '5zqfbSU5i2cu0dicNs8SpU', '2hCgbDmQ3PcDuBlg98kRCH', '2lx0k1fewonWUZuio3ySan', '6fvMzYCz50o7gZ1BrNGU0g', '2xN8XHOVaaIzlxr3WO7dxo', '5xRr6JVdg8QXYIysbvgZtN', '5Lb3trabd1NEinVk8UQerj', '1phvUuZvEqXhu8WE7MaEFK', '1M6yLkfVryssdEXWxE1cYU', '7F7LtxTGFZeQc519EXM3Fz', '2H05ducHR1JFjfFzd8Ci7y', '6EtdGxidyHotHoeKlLbYn4', '5WwsvgQRNKeV1AP2ESU3BM', '708eSRhKO5kZNYYj8TTshm', '1vbUoFcjwCnWhvFhaRl6XW', '0546X8uFGthDWtNSKQRqp1', '5OaCQ4XinbGtR6TbZfcHcu', '7f714xHeYc0JPmy0fFfpeq', '0ax5HgHyWEcXMIoIBdJ6HL', '6atnPmXeJnTOwKCAr96pFt', '3I5phWeVZoLu0SjgdN3WiI', '1LcCePwGpFxjGNS4LmXk6A', '2ZsIYBYJDCK2Or3EcfWHlm', '68IVtAILkqevon0U3ajQNX', '0qhyc4evtEoCnbw8WJDkct', '7qJXtW4COsde0dQXzm4HI8', '1h8VZAl4DMPDPZFVMvbaCt', '6PG9OLPdUuavohyTDJddeA', '2J4alrQQFeqvanDyckHhG7', '3Hhn4g871xkqk80s77cmMy', '3O8Dd4CObbA8TC1WUTnIbC', '04RSm7MR5jUNm15tw64iH2', '1kjQa69O4cfsGElRvGUHDb', '1ujbpSvTcdW6PXVisv9TMf', '6PTDxFk4LmDNZjB3ZTVmGE', '66jZOrpPSQjdxMNaebIjW5', '1NMnPohYbttFELPf52rlnN', '4b7RW7wKYvCrrvsI6lexs1', '3d5EvaD7MgDXHp2aDnN5Yq', '6QYZCWD8JRKMODNjK31WYc', '46zo5YiHBhCfUuhWQLxe2R', '26lao4thh1peAzKViwFBH8', '2c5WYGIu2vi76WLtjtB0EJ', '2JRsFEZNOT9n2UQjSos8Ao', '37i9dQZF1DXbkKnGZHv1kf', '5ydK5Lt2AVVDw0oSfIwrow', '2CIJJ5ZukQ5iRhpWwhHuDZ', '2RJ8jJ1xbWaPEOcqzpSFWB', '5AaJyTsSB1fgsOquaFekZm', '1ODVcUT9ZUUTLe0CFcXNcX', '1nxCCM3Xv3hZhMJ5eCQD06', '5YBEfrHKAWe2rgYDXAHfnB', '7M4vQi7trxZkBUv7eH0fOk', '37i9dQZF1DWULaRXVqGMUt', '3CbFUe8QliW527pQR4iODt', '37i9dQZF1DWSTHVqvNCwNq', '0Vg6D13LJd2FKlZAbh6O6r', '1Ryn2YHEe62hAxO56pLpuD', '37i9dQZF1DX7nt6DdNdydo', '5feyfTNB4G9DX7YY18yXIh', '0qFKkxFDYrZVnTC10nn9U4', '1UoObyFVkL3qFNsROuZV2b', '46YEeBQ8KNfSfdU5cVBo1L', '1xL4C6h7kM2x80OZEWpnOD', '0OXJXzSgGqVB41OnQurrLW', '53gwSYUb7teuTy7BWhifw7', '7Lb4aWDhskQYTElbF5Doxr', '37i9dQZF1DXcc6f6HRuPnq', '5buvee7l1dbINx5lQwcksi', '12xzebzBuJJOMrI9hbqHyM', '7FW0IAVYoT0TuNdtEBlKIu', '7mA7Ybhoj3R2XbbOUPFBlO', '0cznH05Fs4ZjH5DYT2HaQW', '1lg8HTVMhiEcfiAr3h4EiK', '1BpuIdCwQcb5EpZUI3HExU', '3JHLOos6AgjW7XD6c73mYa', '42zklis5t3lXZ6q25Omd3j', '7EI3IVMfebDuKJ72fWMfap', '14p1Fr2GjRzOjYi5K2StBZ', '5pTeTvV6mng8vY4ynbuF2B',],
    },
    'balboa': {
        'spread_sheet_id': '1VfRZ8nxUxTip_qfnz7pG__6xtxXhBVDahYZ5DSeb80g',
        'playlist_ids': ['4yF3ktRNbzS3J8hXGAW8Lt', '5HjMfQnnMZ4n3PQTdMyN51', '0Ic5MxOkXWQD5sHkDS5q9l', '0D7hUk29y7NAiildT1d8jW', '1oNMS0XrTtgQwGCmiDdX9J', '7valA1ft5GaFo4uOI0an8z', '7GxIH2wgY4Lk2JZlOIpoc7', '0iZ7fisFJw28iQ6lDfdI2K', '0S66j7w2lNlkTYAhg2G25U', '3A68uJvHo3oUnlu6QASHwD', '7GnULBKb0qBfWlIwjrcNhH', '2eiEguPccOnFpUx2AhWJyC', '56Bup4RnMyWoqviNNigyOQ', '1aIzbh3eFJCqfqqdrfQZDA', '3I5phWeVZoLu0SjgdN3WiI', '1QpZX4ASwrThTeD6wnBeo5', '0fMUBlmzWd7DRUOlsq0Wuo', '1LcCePwGpFxjGNS4LmXk6A', '3O8Dd4CObbA8TC1WUTnIbC', '5YBEfrHKAWe2rgYDXAHfnB', '6mRBXQW6DWflCIu03GNT4n', '4izFE6UhsUJhMhx2kLGkfY', '1JQ0KjRt89gy0BquY5WEWz', '3lzu8F4Ahm0EM45RmYMuiX', '1I17Oxv9yZSkSnEGwhvqQK', '0fcYVtGB0rdOUL5OfUUAcE', '3CZ0smAQeq7pi1oX0qMYRY', '7t7FUvfqS8okdBrnstwrZD', '3hNbMKZPkAzM01gr6itQhh',],
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
            music_m.update_tracks_to_spreadsheet(
                playlist_ids='',
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


if __name__ == '__main__':
    # cli()
    bpm = music_m.AubioBPMDetector('77ulklR6wxK0Sxc2igNUmG').get_bpm()
    print(bpm)
    # print(SpotifyService().get_track_ds(['1NMnPohYbttFELPf52rlnN']))
    # target_bpms = [180, 170, 75, 80, 190, 200, 90, 80, 200, 210, 180, 80, 75, 210, 220, 85, 75, 200, 190, 80, 80, 180, 190, 90, 80, 180, 190, 90, 95, 180, 210, 200, 85, 95, 195, 185, 100, 95, 180, 190, 90, 95, 200, 210, 90, 85, 200]
    # create_playlist('2023-03-29 Balboa Socail Vol.1', '2 Balboa, 2 SlowBal', target_bpms, 140, to_shuffle=True)

    # playlist_items = SpotifyService().get_all_playlist_items()
    # print(playlist_items[0])

    # music_m.update_playlists_to_spreadsheet(spreadsheet_id=SPOTIFY_ALL_PLAYLIST_SPREADSHEET_ID, sheet_range='Playlist!A2')

    # print(f'{len(playlists)}: {playlists[0]}')
    # playlist_id = ['1vbUoFcjwCnWhvFhaRl6XW', ]
    # spreadsheet_id = '1YrL6UVXXUChtqf4HdgfKU1nnzPX1SX_KsxaW3-Wf33w'
    # DJHelper.update_items_to_sheet(playlist_id, spreadsheet_id)
