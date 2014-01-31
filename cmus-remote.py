#!/usr/bin/env python
# cmus-remote, your own cmus remote control you can access
# from everywhere.
# Uncopyrighted. Enric Morales 2014

from flask import Flask, render_template
from backend import Cmus
from ConfigParser import ConfigParser

cmus = Cmus()
app = Flask(__name__)

config = ConfigParser()
config.read('cmus-remote.ini')
path = config.get('main', 'path')

@app.route("/")
def index():
    if cmus.is_socket_alive():
        actions = ['prev', 'play', 'pause', 'stop', 'next']
        status = cmus.status()

        if status['paused']:
            hilite = "pause"
        elif status['playing']:
            hilite = "play"
        elif status['stopped']:
            hilite = "stop"
        else:
            hilite = None

        return render_template('index.html',
                               actions=actions,
                               hilite=hilite,
                               path=path,
                               status=status)
    else:
        return render_template('error.html')


@app.route('/<action>')
def do_action(action):
    if cmus.is_socket_alive():
        status = cmus.status()
        actions = {'prev': cmus.prev,
                   'play': cmus.play,
                   'next': cmus.nnext,
                   'pause': cmus.pause,
                   'stop': cmus.stop}

        if action in actions:
            message = actions[action]()
        else:
            message = "No such action '%s'" % action

        return render_template('index.html',
                               status=status,
                               path=path,
                               message=message)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    app.debug = True
