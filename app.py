import flask
import pathlib
import os

import backend

app = flask.Flask(__name__, static_url_path='/static')


class EntryNotFoundException(Exception):
    pass


@app.route("/", endpoint='indexhtml')
def indexhtml():
    return app.send_static_file('index.html')

@app.route("/<path:path>", endpoint='index')
def index(path):
    print(path)
    return app.send_static_file(path)

@app.route("/editor",endpoint='editor')
def editor():
    conn = backend.get_db()
    entries = backend.get_entries(conn)
    print(entries)
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