import time
import subprocess
from threading import Timer

class ControlGPIOTest():
    
    def __init__(self):
        print('TEST set up mode board')
        

    def prepare(self):
        pass

    def turn_on_led(self, lednum, ledOn):
        # param True: led on, False, led off
        print('turn on led {} to {}'.format(lednum, ledOn))

    def set_leds_to(self, ledOn):
        print('turning on all LEDS to {}'.format(ledOn))

    def stop(self):
        self.set_leds_to(False)
        print('stop GPIO')

    def btn_new_round(self):
        selected = input('New round ? y/N:')
        if selected == 'y':
            return True
        else:
            return False

    def set_ready_led(self, status):
        print('setting ready led to {}'.format(status))

    def btn_new_photo(self):
        selected = input('New photo ? y/N:')
        if selected == 'y':
            return True
        else:
            return False

    def btn_left(self):
        selected = input('Go Left ? y/N:')
        if selected == 'y':
            return True
        else:
            return False

    def btn_right(self):
        selected = input('Go Right ? y/N:')
        if selected == 'y':
            return True
        else:
            return False
        
    

class CameraTest():
    path = '/home/javier/tests/photo_tmp/'

    def __init__(self):
        print('starting camera')

    def prepare(self):
        time.sleep(3)
        print('camera ready!')
        return self.path

    def capture(self, num_id):
        subprocess.run(["wget", "https://picsum.photos/1024/720"])
        subprocess.run(["mv", "720", self.path + "picture" + str(num_id) + '.jpg'])
        time.sleep(2)
        print('picture taken')
        return 'picture' + str(num_id) + '.jpg'

    def stop(self):
        print('closing camera')
