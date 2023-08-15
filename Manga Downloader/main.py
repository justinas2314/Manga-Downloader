import os
import sys
import time
import collections

import requests
import bs4
import dotenv


def get_urls(base_url, reverse=True):
    r = requests.get(base_url)
    assert r.status_code == 200
    soup = bs4.BeautifulSoup(r.text, features='lxml')
    urls = []
    for ul in soup.find_all('ul'):
        urls.append([])
        for li in ul.find_all('li'):
            try:
                t = li.find('a').get('href')
            except AttributeError:
                continue
            if t not in urls[-1]:
                urls[-1].append(t)
    output = max(urls, key=len)
    return list(reversed(output)) if reverse else output


def get_image_urls(page_url):
    r = requests.get(page_url)
    assert r.status_code == 200
    soup = bs4.BeautifulSoup(r.text, features='lxml')
    urls = []
    for div in soup.find_all('div'):
        counts = collections.defaultdict(lambda: [])
        for img in div.find_all('img'):
            src = img.get('src')
            if src is None or not src.startswith('http'):
                continue
            try:
                counts[src.split('//')[1].split('/')[0]].append(src)
            except IndexError:
                continue
        try:
            urls.append(max(counts.values(), key=len))
        except ValueError:
            continue
    return max(urls, key=len)


def download_images(urls, base_path, timeout):
    with requests.Session() as session:
        for ind, url in enumerate(urls):
            time.sleep(timeout)
            r = session.get(url)
            assert r.status_code == 200
            with open(os.path.join(base_path, f'{str(ind)}.{r.headers["Content-Type"].split("/")[-1]}'), 'wb') as f:
                f.write(r.content)


def tryer_wrapper(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as err:
            print(f"ERROR: '{err}' OCCURED"
                  + (f"\nWHEN EXECUTING: '{func.__name__}'({args}, {kwargs})" if DEBUG == 'TRUE' else "") +
                  f"\nIGNORING WITH TIMEOUT: {ERROR_TIMEOUT}")
            time.sleep(ERROR_TIMEOUT)


def download_everything():
    try:
        os.mkdir(LOCATION)
    except FileExistsError:
        pass
    relative_root = os.path.join(LOCATION, TITLE)
    try:
        os.mkdir(relative_root)
    except FileExistsError:
        pass
    urls = tryer_wrapper(get_urls, BASE_URL, REVERSE)
    for ind, url in enumerate(urls):
        print(ind + 1)
        image_urls = tryer_wrapper(get_image_urls, url)
        location = os.path.join(relative_root, str(ind + 1))
        try:
            os.mkdir(location)
        except FileExistsError:
            pass
        tryer_wrapper(download_images, image_urls, location, TIMEOUT)


if __name__ == '__main__':
    dotenv.load_dotenv()
    DEBUG = os.getenv('DEBUG')
    LOCATION = os.getenv('LOCATION')
    TIMEOUT = float(os.getenv('TIMEOUT'))
    ERROR_TIMEOUT = float(os.getenv('ERROR_TIMEOUT'))
    BASE_URL = sys.argv[1]
    TITLE = sys.argv[2]
    try:
        REVERSE = bool(sys.argv[3])
    except IndexError:
        REVERSE = True
    download_everything()
