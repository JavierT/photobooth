from picamera import PiCamera
import time

class Camera():
    path = '/home/pi/photo_tmp/'

    def __init__(self):
        self.camera = PiCamera()

    def prepare(self):
        # self.camera.start_preview()
        time.sleep(3)
        print('ready!')
        return self.path

    def capture(self, num_id):
        self.camera.capture(self.path + 'picture' + str(num_id) + '.jpg', format='jpeg')
        time.sleep(2)
        print('picture taken')
        return 'picture' + str(num_id) + '.jpg'

    def stop(self):
        print('closing camera')
        self.camera.stop_preview()
        self.camera.close()
