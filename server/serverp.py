import os
import time
import tornado.ioloop
import tornado.web
import threading
from resources import url_patterns
from utils.observer import Subject
from components.control_gpio import ControlGPIO
from components.camera import Camera
from components.collage import Collage


class TornadoApplication(tornado.web.Application):
    """
    Application definition
    """

    def __init__(self):
        try:
            self.main_path = os.path.dirname(__file__)
            # initialize camera, gpio and so on
            self.camera = Camera()
            self.cGPIO = ControlGPIO()
            self.collage = Collage(1024, 720, 20)
            self.new_collage = Subject(None)
            self.running = threading.Event()
            self.th_wait_and_capture = threading.Thread(target=self.wait_and_capture, args=[self.running])
            # self.th_wait_and_capture.start()
            self.th_btns_input = threading.Thread(target=self.process_btn_action, args=[self.running])
            # self.th_btns_input.start()
            tornado.web.Application.__init__(self, url_patterns)
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

    def process_btn_action(self, running_cond):
        while not running_cond.is_set():
            btn_reset = self.cGPIO.btn_new_round()
            #btn_left = self.cGPIO.btn_left()
            #btn_right = self.cGPIO.btn_right()
            
    def wait_and_capture(self, running_cond):
        print('starting...')
        self.capturing = False
        self.cGPIO.prepare()
        self.path = self.camera.prepare()
        self.cGPIO.set_ready_led(True)
        while not running_cond.is_set():
            btn_state = self.cGPIO.btn_new_round()
            if btn_state == False and not self.capturing:
                print('Starting new round!')
                self.cGPIO.set_ready_led(False)
                self.capturing = True
                self.start_new_round()
                self.capturing = False
                self.cGPIO.set_ready_led(True)
            time.sleep(.1)
        print("finishing wait and capture thread")
    
    def start_new_round(self):
        a_images = []
        i = 0
        while i < 4:
            btn_state = self.cGPIO.btn_new_photo()
            print('Waiting for photobtn ', btn_state)
            if btn_state == False:
                print('Starting new photo!')
                self.cGPIO.turn_on_led(i, True)
                a_images.append(self.camera.capture(i))
                time.sleep(0.5)
                i += 1
            time.sleep(.1)
            
        print(a_images)
        imgname = self.collage.create(self.path, a_images)
        time.sleep(2)
        self.cGPIO.set_leds_to(False)
        self.new_collage.next(imgname)
        
if __name__ == "__main__":
    try:
        app = TornadoApplication()
        app.listen(5002)
        tornado.ioloop.IOLoop.current().start()
    except (KeyboardInterrupt):
        print('Detected KeyboardInterrupt')
        app.stop()
        # app.fermeture_application()
