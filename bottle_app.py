# A very simple Bottle Hello World app for you to get started with...
import bottle
from bottle import route, static_file, request
import parser
import page_creator


# Updates everything
def update():
    # Update lectures.json
    parser.update_lectures()


@route('/')
def index():
    return static_file('index.html', root='./static')

# TODO: Complete the response to post requests.
# @route('prerequisitePage', method='post')
# def return_page():
#     return static_file(request.forms.get('subj'), root='./static')


@route('/css/<filepath>')
def css_static(filepath):
    return static_file(filepath, root='./static/css')




application = bottle.run()


