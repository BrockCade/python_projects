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
global current_song
current_song = None
#initilize
def initilize():
    #initilize rotary encoder
    subprocess.call('sudo /bin/python /home/brockc09/headunit/python/headunit_v2/rotary_encoder.py', shell=True)
threading.Thread(target=initilize).start()

sleep(0.5)
view_logic().display_menu(*curser().start())


def displaying_song():
    previus_song = None
    while True:
        sleep(0.1)
        if current_song == previus_song:
            pass
        else:
            LCDView().print_to_lcd(current_song,True,2)
            previus_song = current_song
        gpios = [18,8,10,16,12]
        for gpio in gpios:
            if GPIO.input(gpio) == GPIO.HIGH:
                print('gpio',gpio,'pressed')
                LCDView().print_to_lcd('                    ',True,2)
                return
                    
def song_playing():
    global current_song
    previus_song = None    
    while True: 
        if song_handler.check_song() == previus_song:
            pass
        else:
            current_song = song_handler.check_song()       
threading.Thread(target=song_playing).start()

# Start main event loop
while True:
    
    if GPIO.input(32) == GPIO.LOW:
        displaying_song()
        sleep(0.2)


    if GPIO.input(18) == GPIO.HIGH:# Select button pressed
        print('select')
        curser().selecter()

    if GPIO.input(8) == GPIO.HIGH:# Up button pressed
        print('up')
        view_logic().display_menu(*curser().curser_direction('up'))

    if GPIO.input(10) == GPIO.HIGH:# Down button pressed
        print('down')
        view_logic().display_menu(*curser().curser_direction('down'))

    if GPIO.input(12) == GPIO.HIGH:# left button pressed
        print('left')
        curser().curser_direction('left')


    if GPIO.input(16) == GPIO.HIGH:# right button pressed
        print('right')
        curser().curser_direction('right')


    