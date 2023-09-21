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

GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#rotary encoder button

def displaying_song():
    previus_song = None
    print ('displaying song')
    
    while True:
        
        gpios = [18,8,10,16,12]
        for gpio in gpios:
            if GPIO.input(gpio) == GPIO.HIGH:
                print('gpio',gpio,'pressed')
                LCDView().print_to_lcd('                    ',True,2)
                exit()
        if song_handler.check_song() == previus_song:
            pass
        else:
            previus_song = song_handler.check_song()
            LCDView().print_to_lcd(song_handler.check_song(),True,2)

displaying_song()