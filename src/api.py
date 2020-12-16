#!/usr/bin/env -S PATH="${PATH}:/usr/local/bin" python3

import json
from notion_api import append_note, append_task, append
from bing_api import daily_image_url
from datetime import datetime

from flask import Flask, request, redirect
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


@app.route('/add', methods=['POST'])
def add_generic():
    try:
        content = request.get_json(silent=True) // Added silent=True
    except:
        print('Content: ')
        print(request.data)
        return 'This request must be in json format'
    
    if content is None:
        return 'No content or invalid json supplied'
    elif "title" not in content:
        return '"title" is a required field'
    else:
        try:
            errors = append(content)
            if(len(errors) > 0):
                return json.dumps(errors, indent=4), 200
            else:
                return 'Succeceed in adding data', 200
        except Exception as e:
            return str(e), 500


def add(data_type, request):
    try:
        content = request.get_json(silent=True) // Added silent=True
    except:
        print(request.data)
        title = request.args.get('title')
        if title is None:
            return 'ADD: No '+data_type+' supplied', 400
        else:
            content = {"title": title}
    
    if content is None or "title" not in content:
        return 'ADD2: No '+data_type+' supplied', 400
    else:
        try:
            #send content to notion
            errors = {}
            if data_type == "Task":
                errors = append_task(content)
            else:
                errors = append_note(content)

            if(len(errors) > 0):
                return str(errors), 500
            else:
                return 'Succeceed in adding '+data_type, 200
        except Exception as e:
            return str(e), 500


# redirects to the bing image of the day
@app.route('/bing', methods=['GET'])
def bing():
    try:
        return redirect(daily_image_url(datetime.today().strftime('%Y-%m-%d')), code=302)
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run()
