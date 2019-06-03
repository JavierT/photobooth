import os
import tornado.ioloop
import tornado.web
from resources import url_patterns
from utils.observer import Subject


class TornadoApplication(tornado.web.Application):
    """
    Application definition
    """

    def __init__(self):
        self.main_path = os.path.dirname(__file__)
        # initialize camera, gpio and so on
        self.maj_gpio = Subject(None)
        tornado.web.Application.__init__(self, url_patterns)


if __name__ == "__main__":
    try:
        app = TornadoApplication()
        app.listen(5002)
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt):
        print('Detected KeyboardInterrupt')
        #app.fermeture_application()
