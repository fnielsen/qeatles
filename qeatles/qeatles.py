#!/usr/bin/env python
"""
Usage:
  qeatles.py 

Options:
  -h --help  Help

"""

from __future__ import print_function

from os.path import abspath, join, split

import re

import pandas as pd

from brede.data.wikipedia import WikiPage


URL_TITLES = ("https://raw.githubusercontent.com/"
              "fnielsen/qeatles/master/data/titles.csv")


def download_and_write():
    base_path = join(split(abspath(__file__))[0], 'data')
    html_path = join(base_path, 'html')
    text_path = join(base_path, 'text')

    pattern = re.compile(r"[^a-zA-Z0-9,.' ()\-]")

    titles = read_titles()
    for title in titles['Page']:
        wiki_page = WikiPage(title)
        sanitized_title = pattern.sub(' ', title)
        assert sanitized_title != ''
        assert sanitized_title != '.'
        assert sanitized_title != '..'

        with open(join(html_path, sanitized_title + '.html'), 'w') as f:
            f.write(wiki_page.to_html().encode('utf-8'))

        with open(join(text_path, sanitized_title + '.txt'), 'w') as f:
            f.write(wiki_page.to_text().encode('utf-8'))

        print(sanitized_title)


def read_titles():
    return pd.read_csv(URL_TITLES)


def main(args):
    """Handle command-line interface."""
    download_and_write()
    exit(0)

    titles = read_titles()
    print(titles.to_csv())


if __name__ == '__main__':
    from docopt import docopt

    main(docopt(__doc__))


