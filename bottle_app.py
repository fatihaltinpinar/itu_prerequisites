# A very simple Bottle Hello World app for you to get started with...
import bottle
from bottle import route
import parser
import page_creator


# Updates everything
def update():
    # Update lectures.json
    parser.update_lectures()


@route('/')
def hello_world():
    return 'Hello from Bottle!'


application = bottle.run()

