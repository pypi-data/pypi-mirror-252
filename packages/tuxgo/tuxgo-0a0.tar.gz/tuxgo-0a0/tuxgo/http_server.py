# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import os
import pathlib
import threading

import flask
import werkzeug.serving

bp = flask.Blueprint('tuxgo-uploader', __name__)

@bp.route('/', methods=['GET'])
def index():
    message = ''.join(flask.get_flashed_messages())
    if message:
        flask.current_app.config['is_shutdown'].set()
    else:
        message = 'Pick image below (will open camera) and submit:'
        
    return f'''\
<!doctype html>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>TuxGo capture image</title>
<body>
    <p>{message}</p>
    <form method="post" enctype="multipart/form-data">
        <p><input name="file" type="file" capture="environment" accept="image/*" /></p>
        <p><input type="submit"></p>
    </form>
</body>
'''

@bp.route('/', methods=['POST'])
def submit():
    file = flask.request.files['file']
    flask.current_app.config['image'] = file.read()
    flask.flash(f'the image was submitted')
#   filename = f'/tmp/download.{file.filename.rsplit(".", 1)[-1].casefold()}'
#   file.save(filename)
#   flask.flash(f'the image was saved at {filename}')
    return flask.redirect(flask.url_for('.index'), 303)

def create_app():
    app = flask.Flask(__name__)
    app.secret_key = os.urandom(16)
    app.config['MAX_CONTENT_LENGTH'] = int(16e6) # 16 MB
    app.config['is_shutdown'] = threading.Event()
    app.register_blueprint(bp)
    return app

def get_image_from_http_server(host='0.0.0.0', port=5000, **kwds):
    app = create_app()
    server = werkzeug.serving.make_server(host, port, app, **kwds)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    app.config['is_shutdown'].wait()
    server.shutdown()
    thread.join()
    return app.config.get('image')

if __name__ == '__main__':
#   create_app().run('0.0.0.0')
    print(repr(get_image_from_http_server()[:100]))
