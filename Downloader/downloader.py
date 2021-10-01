import time
import os
from typing import Optional

import requests


def get_chapters(session: requests.Session, manga_id: str, langs: {str} = None, timeout: float = 1):
    print('caching all chapters', end='\r')
    if langs is None:
        langs = {'en'}
    offset = 0
    # uses a dict so that newer uploads replace older ones
    data = {}
    while True:
        with session.get(f'https://api.mangadex.org/chapter?manga={manga_id}&offset={offset}&limit=100') as r:
            r.raise_for_status()
            json = r.json()
        for i in json['data']:
            if i['attributes']['translatedLanguage'] in langs:
                data[i['attributes']['chapter']] = i
        if offset > json['total']:
            break
        else:
            offset += 100
        time.sleep(timeout)
    return data


def download_chapter(session: requests.Session, chapter, location: str, timeout: float = 1):
    """
    this function raises only if the main mangadex server does not respond correctly
    """
    with session.get(f'https://api.mangadex.org/at-home/server/{chapter["id"]}') as r:
        r.raise_for_status()
        image_server = r.json()['baseUrl']
    os.makedirs(location, exist_ok=True)
    length = len(chapter['attributes']['data'])
    for i, j in enumerate(chapter['attributes']['data']):
        print(f'downloading ch. {chapter["attributes"]["chapter"]} im. {i + 1}/{length}'.ljust(50), end='\r')
        while True:
            try:
                download_image(
                    session,
                    f'{location}/{i}.{j.split(".")[-1]}',
                    f'{image_server}/data/{chapter["attributes"]["hash"]}/{j}',
                    image_server
                )
            except requests.HTTPError:
                # if the server does not respond we change servers
                with session.get(f'https://api.mangadex.org/at-home/server/{chapter["id"]}') as r:
                    r.raise_for_status()
                    image_server = r.json()['baseUrl']
                    time.sleep(timeout)
            else:
                break
        time.sleep(timeout)


def download_image(session: requests.Session, location: str, url: str, image_server_for_reporting: str):
    with session.get(url) as r:
        content_length = len(r.content)
        elapsed_time = r.elapsed.microseconds
        try:
            cache = 'HIT' in r.headers['x-cache']
        except TypeError:
            cache = False
        try:
            r.raise_for_status()
        except requests.HTTPError:
            report_to_mangadex(session, image_server_for_reporting, False, cache, content_length, elapsed_time)
            raise
        else:
            data = r.content
    with open(location, 'wb') as f:
        f.write(data)
    report_to_mangadex(session, image_server_for_reporting, True, cache, content_length, elapsed_time)


def report_to_mangadex(session: requests.Session, image_server: str, success: bool,
                       cache: bool, content_length: int, duration: float):
    try:
        session.post('https://api.mangadex.network/report', json={
            'url': image_server,
            'success': success,
            'bytes': content_length,
            'duration': int(duration // 1000),
            cache: cache
        })
    except requests.HTTPError:
        # don't care that much about this
        pass


def download_everything(manga_id: str, location: str, timeout: float, langs: {str},
                        chapter_floor: Optional[float] = None, chapter_ceiling: Optional[float] = None):
    check = {
        (True, True): lambda x: chapter_floor <= float(x) <= chapter_ceiling,
        (True, False): lambda x: chapter_floor <= float(x),
        (False, True): lambda x: float(x) <= chapter_ceiling,
        (False, False): lambda _: True
     }[(chapter_floor is not None, chapter_ceiling is not None)]
    with requests.Session() as session:
        for k, v in sorted(get_chapters(session, manga_id, langs, timeout).items(), key=lambda x: float(x[0])):
            try:
                if check(k):
                    download_chapter(session, v, f'{location}/{k}', timeout)
            # not 100% percent sure every chapter can be converted to a float
            except TypeError:
                download_chapter(session, v, f'{location}/{k}', timeout)
    # the console shoudln't look buggy if i do this
    print(100 * ' ', end='\r')
