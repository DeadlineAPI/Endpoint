import flask
import pathlib
import os
import json

from datetime import datetime
import backend

app = flask.Flask(__name__, static_url_path='/static')


class EntryNotFoundException(Exception):
    pass

@app.template_filter('datefilter')
def _jinja2_filter_date(datestr, fmt=None):
    try:
        date = datetime.strptime(datestr,"%Y-%m-%d")
        return date.strftime('%d. %b %Y')
    except:
        return f"date unparsable: {datestr}"

@app.template_filter('datetimefilter')
def _jinja2_filter_date(datestr, fmt=None):
    try:
        date = datetime.strptime(datestr,"%Y-%m-%d %H:%M:%S %z")
        return date.strftime('%d. %b %Y %H:%M:%S %z')
    except:
        return f"datetime unparsable: {datestr}"

@app.route("/", endpoint='indexhtml')
def indexhtml():
    return app.send_static_file('index.html')

@app.route("/deadlineapi.json", endpoint='deadlineapijson')
def deadlineapijson():
    conn = backend.get_db()
    rows = backend.get_entries(conn)
    conn.close()

    templatefile = open(os.path.join('static','deadlineapi-template.json'),'r')
    template = json.load(templatefile)

    template['deadlines'] = [dict(ix) for ix in rows]
    return flask.jsonify(template)

@app.route("/<path:path>", endpoint='index')
def index(path):
    print(path)
    return app.send_static_file(path)

@app.route("/editor",endpoint='editor')
def editor():
    conn = backend.get_db()
    entries = backend.get_entries(conn)
    return flask.render_template('editor.html',entries=entries)

@app.route("/editor/edit/<int:id>",endpoint='editor_edit_entry', methods=['GET'])
def editor_edit_entry(id):
    id = int(id)
    conn = backend.get_db()
    entry = backend.get_entry(conn,id)
    return flask.render_template('editor_edit_entry.html',entry=entry)

@app.route("/editor/edit/<int:id>",endpoint='editor_save_entry', methods=['POST'])
def editor_edit_entry_save(id):
    to_save_entry = flask.request.form
    id = int(id)
    conn = backend.get_db()
    try:
        entry = backend.get_entry(conn,id)
    except:
        raise EntryNotFoundException("Entry not in DB!")

    backend.edit_entry(conn, to_save_entry, id)
    return flask.redirect('/editor')

@app.route("/editor/new",endpoint='editor_add_entry', methods=['GET'])
def editor_add_entry():
    return flask.render_template('editor_add_entry.html')

@app.route("/editor/new",endpoint='editor_add_entry_save', methods=['POST'])
def editor_add_entry_save():
    to_add_entry = flask.request.form
    conn = backend.get_db()
    backend.add_entry(conn, to_add_entry)
    return flask.render_template('editor_added_entry.html', entry=to_add_entry)

@app.route("/editor/delete/<int:id>",endpoint='editor_delete_entry', methods=['GET'])
def editor_edit_entry_save(id):
    id = int(id)
    conn = backend.get_db()
    try:
        entry = backend.get_entry(conn,id)
    except:
        raise EntryNotFoundException("Entry not in DB!")
    backend.delete_entry(conn, id)
    
    return flask.render_template('editor_deleted_entry.html',entry=entry)

if __name__ == "__main__":
    app.run()