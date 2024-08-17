from pathlib import Path
from typing import Annotated, Callable

import typer

from mozyq.fs import fs
from mozyq.types import Images


def albums_jsonl(wh: int):
    import json

    from cattrs import unstructure

    from mozyq.client import Client

    client = Client.from_file(fs.credentials_json, wh)
    with open(fs.albums_jsonl, 'w') as f:
        for album in client.albums():
            album = unstructure(album)
            print(json.dumps(album), file=f)


def load_albums():
    import json

    from cattrs import structure

    from mozyq.client import Album

    with open(fs.albums_jsonl) as f:
        for line in f:
            yield structure(
                json.loads(line),
                Album)


def album_ids():
    return [album.id for album in load_albums()]


def pool_path():
    return [
        str(fs.album(album.id))
        for album in load_albums()] + [

        str(folder)
        for folder in fs.photos.iterdir()]


AlbumId = Annotated[str, typer.Argument(autocompletion=album_ids)]
PoolPath = Annotated[
    Path,
    typer.Argument(autocompletion=pool_path)]

# @app.command()


def list_albums(wh: int = 630):
    if not fs.albums_jsonl.exists():
        albums_jsonl(wh)

    for album in load_albums():
        print(
            album.mediaItemsCount,
            album.id,
            album.title)


# @app.command()
def download_album(album_id: AlbumId, wh: int = 630, num_pages: int = 100):
    from mozyq.client import Client

    client = Client.from_file(fs.credentials_json, wh)
    client.download_album(album_id, num_pages=num_pages)


def make_dataset(pool: Path, *filters: Callable[[Images], Images]):
    import cv2
    from tqdm import tqdm

    from mozyq.mpp import img_hash, load_images

    out = Path('dataset') / pool
    out.mkdir(exist_ok=True, parents=True)

    imgs = load_images(pool)
    imgs = tqdm(imgs)
    imgs = img_hash(imgs)

    for filter in filters:
        imgs = filter(imgs)

    for i, (img, _) in enumerate(imgs):
        img = img.numpy_view()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        cv2.imwrite(f'{out}/{i:04d}.jpg', img)


# @app.command()
def dataset_all():
    from mozyq import mpp
    make_dataset(
        fs.photos / 'ALL',
        mpp.sharp,
        mpp.colorful)


# @app.command()
def dataset(folder: PoolPath):
    from mozyq import mpp
    make_dataset(
        folder,
        mpp.sharp,
        mpp.colorful)


# @app.command()
def download_photos(wh: int = 630):
    from mozyq.client import Client

    client = Client.from_file(fs.credentials_json, wh)
    client.download_photos(
        out_folder='ALL',
        num_pages=30,
        exclude_cats=[
            'DOCUMENTS',
            'NIGHT',
            'RECEIPTS',
            'SCREENSHOTS',
            'SPORT',
            'UTILITY',
            'WHITEBOARDS'])
