import RPi.GPIO as GPIO
import time

class ControlGPIO():
    ledAzul     = 25
    LedRojo     = 7
    ledAmarillo = 8
    ledBlanco   = 11
    ledVerde    = 4

    btnRojoNext   = 23
    btnAzulBack   = 24
    btnNegroStart = 10
    btnPhoto      = 9

    photoLedOrder = [
        ledAzul,
        LedRojo,
        ledAmarillo,
        ledBlanco
    ]

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        print('set up mode board')

    def prepare(self):
        GPIO.setup(self.ledAzul, GPIO.OUT)
        GPIO.setup(self.LedRojo, GPIO.OUT)
        GPIO.setup(self.ledAmarillo, GPIO.OUT)
        GPIO.setup(self.ledBlanco, GPIO.OUT)
        GPIO.setup(self.ledVerde, GPIO.OUT)

        GPIO.setup(self.btnRojoNext, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnAzulBack, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnNegroStart, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.btnPhoto, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.set_leds_to(False)

    def turn_on_led(self, lednum, ledOn):
        # param True: led on, False, led off
        led = self.photoLedOrder[lednum]
        print('turn on led {}'.format(led))
        GPIO.output(led, ledOn)

    def set_leds_to(self, ledOn):
        GPIO.output(self.ledAzul, ledOn)
        GPIO.output(self.LedRojo, ledOn)
        GPIO.output(self.ledAmarillo, ledOn)
        GPIO.output(self.ledBlanco, ledOn)
        GPIO.output(self.ledVerde, ledOn)

    def stop(self):
        self.set_leds_to(False)
        GPIO.cleanup()

    def btn_new_round(self):
        return GPIO.input(self.btnNegroStart)

    def set_ready_led(self, status):
        GPIO.output(self.ledVerde, status)

    def btn_new_photo(self):
        return GPIO.input(self.btnPhoto)

    def btn_left(self):
        return GPIO.input(self.btnAzulBack)

    def btn_right(self):
        return GPIO.input(self.btnRojoNext)
        