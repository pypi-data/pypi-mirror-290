# https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-code
# https://developers.google.com/photos/library/guides/list

import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Iterable

from attr import dataclass
from cattrs import structure
from google.auth.transport.requests import AuthorizedSession
from google.oauth2.credentials import Credentials
from tqdm import tqdm

API = 'https://photoslibrary.googleapis.com/v1'


@dataclass
class Album:
    id: str
    title: str
    productUrl: str
    mediaItemsCount: int
    coverPhotoBaseUrl: str
    coverPhotoMediaItemId: str


@dataclass
class MediaMetadata:
    creationTime: str
    width: int
    height: int

    @property
    def aspect_ratio(self):
        return self.width / self.height

    @property
    def min_dimension(self):
        return min(self.width, self.height)


@dataclass
class MediaItem:
    id: str
    productUrl: str
    baseUrl: str
    mimeType: str
    mediaMetadata: MediaMetadata
    filename: str


class Client:
    def __init__(self, cred: Credentials, wh: int):
        self.session = AuthorizedSession(cred)
        self.wh = wh

        with open('credentials.json', 'w') as f:
            f.write(cred.to_json())

    @classmethod
    def from_file(cls, credentials_json: Path, wh: int):
        with open(credentials_json) as f:
            cred = json.load(f)
            cred = Credentials(cred['access_token'])
            # cred = Credentials.from_authorized_user_info(json.load(f))

        return cls(cred, wh)

    def albums(self):
        res = self.session.get(f'{API}/albums').json()

        return [
            structure(album, Album)
            for album in res['albums']]

    def album(self, album_id: str, num_pages: int):
        body = {'albumId': album_id}

        for media_item in self.media_items(body, num_pages=num_pages):
            if media_item.mimeType == 'image/jpeg':
                yield media_item

    def media_items(self, body: dict, *, num_pages: int, page_size=100):
        def batch(media_items: list[str] | None):
            if not media_items:
                return

            for item in media_items:
                media_item = structure(item, MediaItem)
                if media_item.mediaMetadata.min_dimension < self.wh:
                    continue

                yield media_item

        try:
            body['pageSize'] = page_size
            for _ in range(num_pages):
                res = self.session.post(
                    f'{API}/mediaItems:search',
                    json=body)

                if res.status_code != 200:
                    print(res.json())
                    return

                res = res.json()

                for media_item in batch(res.get('mediaItems')):
                    yield media_item

                page_token = res.get('nextPageToken')
                body['pageToken'] = page_token

                if page_token is None:
                    return

        finally:
            if 'pageToken' in body:
                del body['pageToken']

    def media_item_content(self, item: MediaItem):
        return self.session.get(f'{item.baseUrl}=w{self.wh}-h{self.wh}-c').content

    def download(self, media_items: Iterable[MediaItem], folder: Path):
        folder.mkdir(parents=True, exist_ok=True)

        media_items = [
            media_item
            for media_item in tqdm(media_items, desc='Searching')
            if not (folder / media_item.filename).exists()]

        with ThreadPoolExecutor() as executor:
            jobs = {
                media_item.filename: executor.submit(
                    self.media_item_content, media_item)
                for media_item in media_items}

            for filename, future in tqdm(jobs.items(), desc='Downloading'):
                content = future.result()
                with open(folder / filename, 'wb') as f:
                    f.write(content)

    # def download_photos(
    #         self, *,
    #         out_folder: str,
    #         num_pages: int,
    #         include_cats: list[Category] = [],
    #         exclude_cats: list[Category] = []):

    #     params = {
    #         'filters': {
    #             'mediaTypeFilter': {
    #                 'mediaTypes': ['PHOTO']},

    #             'contentFilter': {
    #                 'includedContentCategories': include_cats,
    #                 'excludedContentCategories': exclude_cats}}}

    #     self.download(
    #         self.media_items(params, num_pages=num_pages),
    #         fs.photos / out_folder)

    def download_album(self, album_id: str, num_pages: int):
        self.download(
            self.album(album_id, num_pages=num_pages),
            Path('albums') / album_id)
