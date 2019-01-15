# A very simple Bottle Hello World app for you to get started with...
import bottle
from bottle import route

@route('/')
def hello_world():
    return 'Hello from Bottle!'


application = bottle.run()

