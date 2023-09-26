from flask import Blueprint, render_template
from flaskwebgui import close_application

web = Blueprint('web', __name__)


@web.route('/')
def hello():
    return render_template('index.html')


@web.route('/close', methods=['GET'])
def close_window():
    close_application()
