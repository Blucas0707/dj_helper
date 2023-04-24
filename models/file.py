import csv
from typing import List


def export_csv(headers: List[str], filename: str, track_ds: List[dict]):
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
