import os

import dotenv
import argparse

from downloader import download_everything

if __name__ == '__main__':
    dotenv.load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('mangadex_id')
    parser.add_argument('name')
    parser.add_argument('chapter_range')
    args = parser.parse_args()
    mangadex_id = args.mangadex_id
    name = args.name
    try:
        chapter_range = list(map(lambda x: float(x) if len(x) else None, args.chapter_range.strip().split('-')))
    except (AttributeError, TypeError, ValueError):
        print('chapter range not specified downloading everything')
        chapter_range = []
    langs = set(map(lambda x: x.strip(), os.getenv('langs').split(',')))
    timeout = float(os.getenv('timeout'))
    root_dir = os.getenv('location')
    download_everything(
        mangadex_id,
        os.path.join(root_dir, name if name is not None else mangadex_id),
        timeout,
        langs,
        *chapter_range
    )
