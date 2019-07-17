#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

import os
from cachetools import cached


@cached(cache={})
def notionToken():
    return os.environ.get('NOTION_TOKEN')


@cached(cache={})
def tasksDatabaseURL():
    return os.environ.get('TASKS_DATABASE_URL')


@cached(cache={})
def notesDatabaseURL():
    return os.environ.get('NOTES_DATABASE_URL')


@cached(cache={})
def maxTitleLength():
    return os.environ.get('MAX_TITLE_LENGTH') or 100
