# Import necessary libraries and modules
from RPi import GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
from Spotify_API import *  # Import Spotify API functionality
import threading  # Import threading module for multithreading
from lcd_view import LCDView  # Import LCDView class from lcd_view module

# Define GPIO pin numbers for the rotary encoder
clk = 38  # Clock pin
dt = 36   # Data pin

# Set GPIO pin numbering mode to BOARD mode
GPIO.setmode(GPIO.BOARD)

# Set up GPIO pins for the rotary encoder with pull-down resistors
# "pull_up_down=GPIO.PUD_DOWN" sets the initial value to be pulled low (off)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialize global variables for the rotary encoder and LCD display
global counter
counter = 0
clkLastState = GPIO.input(clk)

# Function to send volume changes to Spotify and update LCD display
def send_volume():
    while True:
        lastcounter = counter
        if lastcounter == counter:
            pass
        else:
            # Send the new volume value to the Spotify API
            spotifyapi.change_volume(int(counter))
            # Update the LCD display with the current volume
            LCDView().print_to_lcd('volume: ' + str(int(counter)) + '          ', False, 4)

# Start a thread to continuously send volume changes to Spotify and update the display
thread = threading.Thread(target=send_volume)
thread.start()

lap = 0
while True:
    # Read the current state of the rotary encoder pins
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    
    # Check for changes in the rotary encoder state
    if clkState != clkLastState:
        if dtState != clkState:
            if counter != 100:  # Ensure the volume doesn't go above 100
                counter += 1
                sleep(0.01)
        else:
            if counter != 0:  # Ensure the volume doesn't go below 0
                counter -= 1
                sleep(0.01)
    clkLastState = clkState
