try:
    import RPi.GPIO as GPIO
except ImportError:
    # we are in a pc
    class Buttons():

        def __init__(self, on_green, on_blue, on_red):
            pass

        def setGreenLed(self, value):
            pass

        def setRedLed(self, value):
            pass

        def setBlueLed(self, value):
            pass

        def cleanup(self):
            pass
else:
    class Buttons():
        def __init__(self, on_green, on_blue, on_red):
            super(Buttons, self).__init__()

            #Set the Buttons and LED pins
            import os

            self.greenButton = int(os.getenv("GREEN_BTN"))
            self.greenLED = int(os.getenv("GREEN_LED"))

            self.redButton = int(os.getenv("RED_BTN"))
            self.redLED = int(os.getenv("RED_LED"))

            self.blueButton = int(os.getenv("BLUE_BTN"))
            self.blueLED = int(os.getenv("BLUE_LED"))
            
            #Set warnings off (optional)
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.cleanup()
            
            #Setup the Buttons and LEDs
            GPIO.setup(self.greenButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.greenLED,GPIO.OUT)

            GPIO.setup(self.redButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.redLED,GPIO.OUT)

            GPIO.setup(self.blueButton,GPIO.IN,pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.blueLED,GPIO.OUT)
            
            GPIO.output(self.greenLED, False)
            GPIO.output(self.blueLED, False)
            GPIO.output(self.redLED, False)

            GPIO.add_event_detect(self.greenButton, GPIO.RISING, callback=on_green, bouncetime=200)
            GPIO.add_event_detect(self.redButton, GPIO.FALLING, callback=on_red, bouncetime=200)
            GPIO.add_event_detect(self.blueButton, GPIO.FALLING, callback=on_blue, bouncetime=200)
            
        def setGreenLed(self, value):
            GPIO.output(self.greenLED, value)
        
        def setRedLed(self, value):
            GPIO.output(self.redLED, value)
        
        def setBlueLed(self, value):
            GPIO.output(self.blueLED, value)

        def cleanup(self):
            GPIO.cleanup()


