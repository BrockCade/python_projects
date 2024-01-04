# Import necessary libraries
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
from lcd_view import *  # Import LCDView class from lcd_view module
from logic_model import *  # Import logic_model module
import subprocess  # Import subprocess module for running external commands
import threading  # Import threading module for multithreading

# Ignore GPIO warnings
GPIO.setwarnings(False)

# Set GPIO pin numbering mode to BOARD mode
GPIO.setmode(GPIO.BOARD)

# Set up GPIO pins for buttons with pull-down resistors
# "pull_up_down=GPIO.PUD_DOWN" sets the initial value to be pulled low (off)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Select button
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Up button
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Down button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Left button
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Right button
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Rotary encoder button

# Define a global variable for the current song
global current_song
current_song = None

# Initialize the rotary encoder in a separate thread
def initialize():
    subprocess.call('sudo /bin/python /home/brockc09/headunit/python/headunit_v7/rotary_encoder.py', shell=True)

# Start the initialization thread
threading.Thread(target=initialize).start()

# Pause briefly before displaying the initial menu
sleep(0.5)


# Function to continuously display the current song on an LCD
def displaying_song():
    previous_song = None
    while True:
        sleep(0.1)
        if current_song == previous_song:
            pass
        else:
            LCDView().print_to_lcd(current_song, True, 2)
            previous_song = current_song
        gpios = [18, 22, 24, 16, 12]
        for gpio in gpios:
            if GPIO.input(gpio) == GPIO.HIGH:
                print('gpio', gpio, 'pressed')
                update()
                return

# Function to check and update the currently playing song
def song_playing():
    global current_song
    previous_song = None    
    while True: 
        if song_handler.check_song() == previous_song:
            pass
        else:
            current_song = song_handler.check_song()

# Start the thread to monitor and update the currently playing song
threading.Thread(target=song_playing).start()

# Main event loop

while True:

    if GPIO.input(32) == GPIO.LOW: # Rotary encoder button pressed
        displaying_song()
        sleep(0.2)
    
    if GPIO.input(12) == GPIO.HIGH:  # Left button pressed
        print('left')
        Spotify_API.spotifyapi().previous()

    if GPIO.input(16) == GPIO.HIGH:  # Right button pressed
        print('right')
        Spotify_API.spotifyapi().skip()
    
    if GPIO.input(18) == GPIO.HIGH:  # Select button pressed
        print('select')
        select()
         
    if GPIO.input(22) == GPIO.HIGH:  # Up button pressed
        print('up')
        up()

        
    if GPIO.input(24) == GPIO.HIGH:  # Down button pressed
        print('down')
        down()

