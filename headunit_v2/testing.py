import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
from lcd_view import *
from logic_model import *
import subprocess
import threading
# Ignore GPIO warnings
GPIO.setwarnings(False)
# Set GPIO pin numbering mode
GPIO.setmode(GPIO.BOARD)
# Set up GPIO pins for buttons with pull-down resistors
# "pull_up_down=GPIO.PUD_DOWN" sets the initial value to be pulled low (off)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Select button
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Up button
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Down button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#left
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#right

bt = timer()
bt.start()

menu = ['play', 'pause', 'skip','previous   ' ]

def last_press(reset):
    if reset == True:
        bt.start()
        pass
    if bt.stop() > 5:
        bt.start()
        check_song()
        pass
        
    else:
        pass 
    
def check_song():
        while True: # Run forever
            gpios = [18,8,10,12,16]
            for gpio in gpios:
                if GPIO.input(gpio) == GPIO.HIGH:
                    print('gpio',gpio,'pressed to break loop')
                    sleep(0.2)
                    monitor()
                    return
            
            
            LCDView().print_to_lcd(song_handler.check_song() + '                       ',True,4)

def monitor():
    while True:
        
        gpios = [18,8,10,12,16]
        
        for gpio in gpios:
            last_press(False)
            if GPIO.input(gpio) == GPIO.HIGH:
                print('gpio',gpio,'pressed')
                last_press(True)
                sleep(0.2)
                break
        
        sleep(0.1)


monitor()


