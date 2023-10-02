from flaskwebgui import FlaskUI

from abaco import create_app
from abaco.utils import purge_temp_files

if __name__ == '__main__':

    def saybye():
        purge_temp_files()
        print('Bye!')

    FlaskUI(app=create_app(), server='flask', on_shutdown=saybye).run()

    # create_app().run(debug=True)
