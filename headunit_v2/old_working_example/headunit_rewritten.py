# Import necessary libraries
import drivers
# Initialize the LCD display
display = drivers.Lcd()
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
#from Spotify_API import *
import subprocess
import Spotify_API
spotifyapi = Spotify_API.spotifyapi
# Ignore GPIO warnings
GPIO.setwarnings(False)

# Set GPIO pin numbering mode
GPIO.setmode(GPIO.BOARD)

# Set up GPIO pins for buttons with pull-down resistors
# "pull_up_down=GPIO.PUD_DOWN" sets the initial value to be pulled low (off)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Up button
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Down button
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Select button
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#left
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#right

#rotary encoder setup
clk = 38
dt = 36
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)





class headunit():
    def __init__(self) -> None:
        spotifyapi().refresh_access_token()
        self.access_token = spotifyapi().read('access_token')
        #print('read access token')
        self.curser = '->'
        self.curser_pos = 1
        self.page1 = ['play', 'pause', 'skip','previous' ]
        self.page2 = ['refresh_access_token', 'pause4', 'skip3', 'previus2']
        self.counter = 0
        self.check_song()
        
    def print_to_lcd(self,displaying,clear = True,linenum = 1):
        #check if we need to clear the screen
        if clear == True:
            display.lcd_clear()
        elif clear == False:
            pass
        else:
            print('clear not a boolean')

        #check if we are displaying a string or a list
        if type(displaying) == str:
            display.lcd_display_string(displaying, linenum)
        elif type(displaying) == list:
            linenum = 1
            for line in displaying:
                display.lcd_display_string(line, linenum)
                linenum = linenum + 1
        else:
            print('displaying not a string or list')

    def check_song(self):
        playing = ''
        while True: # Run forever
            if GPIO.input(18) == GPIO.HIGH:  # Select button pressed
                break
            
            if spotifyapi().get_currently_playing() != playing:
                if spotifyapi().get_currently_playing() == 'nothing playing':
                    self.print_to_lcd('                    ',False,4)    
                    self.print_to_lcd('nothing playing',False,4)
                    print('nothing playing')
                elif spotifyapi().get_currently_playing() == 'error':
                    self.print_to_lcd('                    ',False,4)    
                    self.print_to_lcd('error',False,4)
                    print('error')
                    break
                else:
                    playing = spotifyapi().get_currently_playing()
                    self.print_to_lcd('                    ',False,4)    
                    self.print_to_lcd(playing,False,4)
                    print(playing)
           


    def menu(self, menuitems):
        volume = 0
        
        clkLastState = GPIO.input(clk)
        # Display menu items on the LCD
        for item in menuitems:
            if menuitems.index(item) != self.curser_pos - 1:
                display.lcd_display_string(item, menuitems.index(item) + 1)
                print('menuitems', menuitems.index(item) + 1)
        
        # Display the cursor and the currently selected menu item
        display.lcd_display_string(self.curser + menuitems[0], 1)
        
        # Main menu loop
        while True:
            if GPIO.input(18) == GPIO.HIGH:  # Select button pressed
                print('select')
                # Call the selected method based on the cursor position
                if menuitems == self.page1:
                    spotifyapi().pick(self.page1[self.curser_pos - 1])
               #        
               #    except:
               #        method = getattr(headunit(), self.page1[self.curser_pos - 1], None)
               #        method()
               #    
               #elif menuitems == self.page2:
               #    try:
               #        method = getattr(self.page2[self.curser_pos - 1], None)
               #        print(method)
               #        method()
               #    except:
               #        method = getattr(headunit(), self.page2[self.curser_pos - 1], None)
               #        method()
                    
                
                #print(method)
                sleep(0.2)

            if GPIO.input(12) == GPIO.HIGH:  # left button pressed
                print('left')
                volume = volume - 10
                self.change_volume(volume)
                display.lcd_display_string('volume: ' + str(volume), 4)
                sleep(0.2)

            if GPIO.input(16) == GPIO.HIGH:
                print('right')
                volume = volume + 10
                self.change_volume(volume)
                display.lcd_display_string('volume: ' + str(volume), 4)
                sleep(0.2)

            if GPIO.input(8) == GPIO.HIGH:  # Up button pressed
                display.lcd_clear()
                self.curser_pos = self.curser_pos - 1
                if self.curser_pos == 0:# if the curser is at the top of the menu go to the next page
                    headunit().menu(headunit().page1)
                print('up', self.curser_pos)
                # Update the displayed menu items
                for item in menuitems:
                    if menuitems.index(item) != self.curser_pos - 1:
                        display.lcd_display_string(item, menuitems.index(item) + 1)
                        print('menuitems', menuitems.index(item) + 1)
                display.lcd_display_string(self.curser + menuitems[self.curser_pos - 1], self.curser_pos)
                sleep(0.2)
                
            if GPIO.input(10) == GPIO.HIGH:  # Down button pressed
                display.lcd_clear()
                self.curser_pos = self.curser_pos + 1
                if self.curser_pos == 5:# if the curser is at the top of the menu go to the next page
                    headunit().menu(headunit().page2)
                print('down', self.curser_pos)
                # Update the displayed menu items
                for item in menuitems:
                    if menuitems.index(item) != self.curser_pos - 1:
                        display.lcd_display_string(item, menuitems.index(item) + 1)
                        print('menuitems', menuitems.index(item) + 1)
                display.lcd_display_string(self.curser + menuitems[self.curser_pos - 1], self.curser_pos)
                sleep(0.2)



# Start the menu with the initial menu items (page1)
class main():
    def __init__(self) -> None:
        #thread = threading.Thread(target=headunit().volume_knob)
        #thread.start()
        #subprocess.run(["xterm", "-e", "/bin/python", r"/home/brockc09/headunit/python/spotify_api/rotary_encoder.py"], env={"DISPLAY": ":0"})
        print('started rotary encoder')
    def start(self):
        headunit().menu(headunit().page1)

if __name__ == '__main__':
    app = main()
    app.start()