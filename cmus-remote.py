#!/usr/bin/env python
# cmus-remote, your own cmus remote control you can access
# from everywhere.
# Uncopyrighted. Enric Morales 2014

from flask import Flask, render_template
from backend import Cmus
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('cmus-remote.ini')
user = config.get('main', 'user')

cmus = Cmus(user)
app = Flask(__name__)


@app.route("/")
def index():
    if cmus.is_socket_alive():
        actions = ['prev', 'play', 'pause', 'next']
        status = cmus.status()

        if status['paused'] or status['stopped']:
            hilite = "pause"
            actions.pop(actions.index('play'))
        else:
            hilite = "play"
            actions.pop(actions.index('pause'))

        return render_template('index.html',
                               actions=actions,
                               hilite=hilite,
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
                               message=message)
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
