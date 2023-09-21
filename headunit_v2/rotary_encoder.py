from RPi import GPIO
from time import sleep
from Spotify_API import *
import threading
from lcd_view import LCDView

clk = 38
dt = 36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

global counter
counter = 0
clkLastState = GPIO.input(clk)
def send_volume():
    while True:
        lastcounter = counter
        if lastcounter == counter:
             pass
        else:
             spotifyapi.change_volume(int(counter))
             LCDView().print_to_lcd('volume: ' + str(int(counter))+'          ',False, 4)
        

thread = threading.Thread(target=send_volume)
thread.start()
lap = 0
while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        
        if clkState != clkLastState:
            if dtState != clkState:
                if counter!=100:     
                    counter += 1
                    sleep(0.01)          
            else:
                if counter!=0:
                    counter -= 1
                    sleep(0.01)
            #print(int(counter))
        clkLastState = clkState
                    
    

