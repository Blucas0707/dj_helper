from typing import Sequence, Iterable
import itertools as it


def divide_by_size(data, size: str):
    if isinstance(data, Sequence):
        for idx in range(0, len(data), size):
            yield data[idx : idx + size]

    elif isinstance(data, Iterable):
        data = iter(data)

        while True:
            chunk = list(it.islice(data, size))
            if chunk:
                yield chunk
            else:
                break

    else:
        raise TypeError('data should be a sequence or iterable')
