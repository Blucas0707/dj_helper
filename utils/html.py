import urllib.parse


def make_query_string(url: str, params_d: dict) -> str:
    query_str = urllib.parse.urlencode(params_d)
    return f'{url}?{query_str}'
