#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

# Heavily borrowed from https://github.com/kevinjalbert/alfred-notion/blob/v1.0.0/src/notion_api.py
# TODO: Would be nice to replace this and the source material with a common package

import json
from cachetools import cached
from datetime import datetime

from notion.client import NotionClient
from notion.block import DividerBlock, TextBlock, CodeBlock, HeaderBlock

from config import notionToken, tasksDatabaseURL, notesDatabaseURL, maxTitleLength


@cached(cache={})
def client():
    return NotionClient(token_v2=notionToken(), monitor=False)


@cached(cache={})
def databaseByURL(url):
    return client().get_collection_view(url)

@cached(cache={})
def tasksDatabase():
    return databaseByURL(tasksDatabaseURL())


@cached(cache={})
def notesDatabase():
    return databaseByURL(notesDatabaseURL())


def append_row(data, collection):
    row = collection.add_row()
    
    # if the title exceeds a max length, put the full title inside the page as
    # a Text Block, then truncate the title
    if len(data["title"]) > maxTitleLength():
        row.children.add_new(TextBlock, title=data["title"])
        data["title"] = data["title"][:maxTitleLength()] + "..."
    
    # get the title out first. This is the main thing. Errors may be possible
    # with the rest of it, so we want to at least get the title down
    row.title = data["title"]
    print(row.title)
    data.pop('title') # don't need to use this twice
    
    # if we have a "body", add that as a text block rather than a property
    if "body" in data:
        row.children.add_new(TextBlock, title=data["body"])
        data.pop('body')

    errors = {}

    for p in data:
        if collection.get_schema_property(p) is not None:
            try:
                row.set_property(p, data[p])
            except Exception as e:

                errors[p] = str(e)
        else:
            errors[p] = "Property '{}' not acceptable for collection '{}' (valid options: {})".format(p, collection.name, [d['name'] for d in collection.get_schema_properties()])
        print(errors[p])
            
    if len(errors) > 0:
        row.children.add_new(DividerBlock)
        row.children.add_new(HeaderBlock, title="Upload errors")
        row.children.add_new(CodeBlock, title=json.dumps(errors, indent=4))
        print('APR - Errors: ')
        print(errors)
    return errors


def append_note(note):
    collection = notesDatabase().collection
    if "type" not in note:
        note["type"] = "Note"
    return append_row(note, collection)


def append_task(task):
    collection = tasksDatabase().collection
    if "type" not in task:
        task["type"] = "Task"
    return append_row(task, collection)


def append(note):
    if "url" in note:
        collection = databaseByURL(note["url"]).collection
        note.pop("url")
    elif "type" in note and note["type"] == "Task":
        collection = tasksDatabase().collection
    else:
        note["type"] = "Note"
        collection = notesDatabase().collection
    return append_row(note, collection)
