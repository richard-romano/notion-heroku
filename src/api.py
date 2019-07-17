#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

from notion_api import append_note, append_task
# from config import importedTagURL

from flask import Flask, request
app = Flask(__name__)


@app.route('/add_note', methods=['GET', 'POST'])
def add_note():
    try:
        return add('Note', request)
    except Exception as e:
        print(str(e))
        return 'Failed in adding note', 500


@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    try:
        return add('Task', request)
    except Exception as e:
        print(str(e))
        return 'Failed in adding task', 500


def add(data_type, request):
    try:
        content = request.get_json()
    except:
        title = request.args.get('title')
        if title is None:
            return 'No '+data_type+' supplied', 400
        else:
            content = {"title": title}
    
    if content is None or "title" not in content:
        return 'No '+data_type+' supplied', 400
    else:
        try:
            #send content to notion
            errors = {}
            if data_type == "Task":
                errors = append_task(content)
            else:
                errors = append_note(content)

            if(len(errors) > 0):
                return errors, 500
            else:
                return 'Succeceed in adding '+data_type, 200
        except Exception as e:
            return str(e), 500

if __name__ == '__main__':
    app.run()
