from RPi import GPIO
from time import sleep
from Spotify_API import *
import asyncio
import threading
import drivers
display = drivers.Lcd()
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
             display.lcd_display_string('volume: ' + str(int(counter))+'          ', 4)
        

thread = threading.Thread(target=send_volume)
thread.start()
lap = 0
while True:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)
        
        if clkState != clkLastState:
            if dtState != clkState:
                if counter!=100:     
                    counter += 0.5
                    sleep(0.01)          
                    
                    
                        
                
            else:
                if counter!=0:
                    counter -= 0.5
                    sleep(0.01)
            #print(int(counter))
        clkLastState = clkState
                    
    

