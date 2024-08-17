from pathlib import Path
from typing import Literal

CacheableSize = Literal[2048, 1024, 512, 256, 128, 64, 32]


class fs:
    credentials_json = Path('credentials.json')
    albums_jsonl = Path('albums.jsonl')

    albums = Path('albums')
    photos = Path('photos')
    dataset = Path('dataset')
    cache = Path('.cache')

    @staticmethod
    def album(album_id: str):
        return fs.albums / album_id
