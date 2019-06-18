import os
import time
import asyncio
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer, socket
from tornado.options import options
import threading
from resources import url_patterns
from utils.observer import Subject
from components.control_gpio import ControlGPIO
from components.camera import Camera
# from components.test_server import ControlGPIOTest, CameraTest
from components.collage import Collage
from resources.ws_actions import ActionsWebSocket
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from resources.h_base import BaseStaticFileHandler


class TornadoApplication(tornado.web.Application):
    """
    Application definition
    """

    def __init__(self):
        try:
            self.main_path = os.getcwd()
            print('main path: {}'.format(self.main_path))
            settings = {
                "static_path": os.path.join(self.main_path, 'public'),
                "xsrf_cookies": True,
            }
            # initialize camera, gpio and so on
            self.camera = Camera()
            self.cGPIO = ControlGPIO()
            self.collage = Collage(1024, 720, 20)
            self.new_collage = Subject(None)
            self.action = Subject(None)
            self.running = threading.Event()
            loop1 = asyncio.new_event_loop()
            self.th_wait_and_capture = threading.Thread(target=self.wait_and_capture, args=[loop1, self.running])
            self.th_wait_and_capture.start()
            loop2 = asyncio.new_event_loop()
            self.th_btns_input = threading.Thread(target=self.process_btn_action, args=[loop2, self.running])
            self.th_btns_input.start()
            url_patterns.append((r"/data/(.*)/?", BaseStaticFileHandler, dict(path=settings['static_path'])))
            print('urls: ', url_patterns)
            tornado.web.Application.__init__(self, url_patterns, **settings)
            self.io_loop = tornado.ioloop.IOLoop.current()
        except Exception as e:
            print('exception in main, ', e)

    def stop(self):
        try:
            self.running.set()
            print('stopping camera')
            self.camera.stop()
        except Exception as e:
            print('Exception deleting camara components ', e)
        try:
            self.cGPIO.stop()
        except Exception as e:
            print('Exception deleting cgpio components ', e)
        self.th_wait_and_capture.join()

    def process_btn_action(self, loop, running_cond):
        asyncio.set_event_loop(loop)

        while not running_cond.is_set():
            #btn_reset = self.cGPIO.btn_new_round()
            btn_left = False
            btn_right = False
            btn_left = self.cGPIO.btn_left()
            btn_right = self.cGPIO.btn_right()
            #if btn_reset:
            #    print('sending action NEW')
            #    self.new_collage.next(ActionsWebSocket.NEW)
            if not btn_left:
                print('sending action NEXT')
                self.action.next(ActionsWebSocket.NEXT)
            elif not btn_right:
                print('sending action BACK')
                self.action.next(ActionsWebSocket.BACK)
            time.sleep(2)
            
    def wait_and_capture(self, loop, running_cond):
        print('starting...')
        asyncio.set_event_loop(loop)
        self.capturing = False
        self.cGPIO.prepare()
        self.path = self.camera.prepare()
        self.cGPIO.set_ready_led(True)
        while not running_cond.is_set():
            btn_state = self.cGPIO.btn_new_round()
            if not btn_state and not self.capturing:
                print('Starting new round!')
                self.cGPIO.set_leds_to(True)
                time.sleep(0.3)
                self.cGPIO.set_leds_to(False)
                time.sleep(0.3)
                self.cGPIO.set_leds_to(True)
                time.sleep(0.3)
                self.cGPIO.set_leds_to(False)

                self.capturing = True
                self.start_new_round()
                self.capturing = False
                self.cGPIO.set_ready_led(True)
            time.sleep(.1)
        print("finishing wait and capture thread")
    
    def start_new_round(self):
        a_images = []
        i = 0
        self.cGPIO.set_ready_led(True)
        print('Waiting for photobtn ')
        while i < 4:
            btn_state = self.cGPIO.btn_new_photo()
            if not btn_state:
                print('Starting new photo!')
                self.cGPIO.set_ready_led(False)
                self.cGPIO.turn_on_led(i, True)
                a_images.append(self.camera.capture(i))
                time.sleep(0.5)
                i += 1
                self.cGPIO.set_ready_led(True)
            time.sleep(.1)
        self.cGPIO.set_ready_led(False)
        print(a_images)
        imgname = self.collage.create(self.path, a_images)
        self.new_collage.next(imgname)
        time.sleep(.5)
        self.cGPIO.set_leds_to(False)

        
if __name__ == "__main__":
    try:
        tornado.platform.asyncio.AsyncIOMainLoop().install()
        app = TornadoApplication()
        #app.listen(5002)
        leserver = HTTPServer(app, max_buffer_size=250000000)
        leserver.bind(5002, family=socket.AF_INET)
        leserver.start()
        
        # tornado.ioloop.IOLoop.current().start()
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt):
        print('Detected KeyboardInterrupt')
        app.stop()
        # app.fermeture_application()
