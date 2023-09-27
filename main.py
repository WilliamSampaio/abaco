from flaskwebgui import FlaskUI
from rich import print as p

from abaco import create_app

if __name__ == '__main__':

    def saybye():
        p('Bye!')

    FlaskUI(app=create_app(), server='flask', on_shutdown=saybye()).run()
