from flaskwebgui import FlaskUI

from abaco import create_app

if __name__ == '__main__':

    def saybye():
        print('Bye!')

    FlaskUI(app=create_app(), server='flask', on_shutdown=saybye).run()

    # create_app().run(debug=True)
