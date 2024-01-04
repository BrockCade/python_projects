from lcd_view import *
import Spotify_API
from time import sleep
# Import necessary libraries
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
import socket
import os

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



#playlist1 = Spotify_API.spotifyapi().playlists()
#print(playlist1['Best of nickleback'])
playlists = False

menu = []
temp_menu = []
active_page = 1





class menu_item():
    
    def __init__(self,name,position,page):
        self.position = position
        self.name = name
        self.page = page
        
    def show(self):
        if len(self.name) > 20:
            self.name = self.name[:20]
            print(self.name)
        LCDView.clear_line(LCDView,self.position)
        LCDView.print_to_lcd(LCDView,self.name,False,self.position)
        
    def cursor_show(self):
        if len(self.name) > 18:
            self.name = self.name[:18]
            print(self.name)
        LCDView.clear_line(LCDView,self.position)
        LCDView.print_to_lcd(LCDView,'->' + self.name,False,self.position)
        
    def show_page(page):
        LCDView.clear_display(LCDView)
        for item in menu:
            if item.page == active_page:
                item.show()
        menu[curser.position + curser.page].cursor_show()




class menu_item_play(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('play')
        Spotify_API.spotifyapi().play()

class menu_item_pause(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('pause')
        Spotify_API.spotifyapi().pause()
        
class menu_item_skip(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('skip')
        Spotify_API.spotifyapi().skip()
        
class menu_item_previous(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('previous')
        Spotify_API.spotifyapi().previous()
        
class menu_item_ip(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('ip')
        print(socket.gethostbyname(socket.gethostname()))
        
class menu_item_home(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name,position,page)

    def action(self):
        print('home')
        global active_page
        global menu
        global temp_menu
        global playlists
        menu.clear()
        for item in temp_menu:
            menu.append(item)
        active_page = 1
        curser.page = 0
        curser.position = 0
        playlists = False
        print('temp_menu',temp_menu)
        print(menu)
        menu_item.show_page(active_page)
   
class menu_item_curser(menu_item):
    def __init__(self, name, position,page):
        super().__init__(name,position,page)
        
    def up(self):
        global active_page
        
        if curser.position == 0:
            if curser.position +1 != active_page:
                curser.position = 3
                active_page -= 1
                curser.page -= 4
                menu_item.show_page(active_page)
                return
        else:
            menu[curser.position + curser.page].show()
            curser.position -= 1
            menu[curser.position + curser.page].cursor_show()
            
            
    def down(self):
        global active_page
        
        if curser.position == 3:
            curser.position = 0
            active_page += 1
            curser.page += 4
            menu_item.show_page(active_page)
            return
        else:
            if curser.position + curser.page == len(menu) - 1:
                return
            menu[curser.position + curser.page].show()
            curser.position += 1
            menu[curser.position + curser.page].cursor_show()

class menu_item_playlist(menu_item):
    def __init__(self, name, position,page ,id = None):
        self.id = id
        super().__init__(name, position, page)

    def get_playlists(self):
        global playlists
        global active_page
        global temp_menu
        global menu
        
        playlists_info = Spotify_API.spotifyapi().playlists()
        counter = 1
        page_counter = 1
        temp_menu.clear()
        for item in menu:
            temp_menu.append(item)
        menu.clear()
        print(temp_menu)
        playlists = True
        for playlist in playlists_info: 
            #print(playlist)
            menu.append(menu_item_playlist(playlist,counter,page_counter,playlists_info[playlist]))
            counter += 1
            if counter >= 5:
                counter = 1
                page_counter += 1
            sleep(1)
        menu.append(menu_item_home('home',counter ,page_counter))
        for item in menu:
            print(item.page)
    def playlist_info(self):
        print(self.name)
        print(self.id)
        print(self.position)
  
    def action(self):
        global playlists
        global active_page
        global temp_menu

        if playlists == False:
            self.get_playlists()
            active_page = 1
            curser.page = 0
            
            menu_item.show_page(active_page)
        
        else:
            Spotify_API.spotifyapi().play_item(self.id,'playlist')
        
        
class menu_item_devices(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name, position, page)

    def action(self):
        print('devices')
        Spotify_API.spotifyapi().devices()
        
class menu_item_shuffle(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name, position, page)
        self.previous_state = None
        
    def action(self):
        if self.previous_state == 'true':
            Spotify_API.spotifyapi().shuffle('false')
            self.previous_state = 'false'
            self.name = 'shuffle off'
            self.show()
        else:
            Spotify_API.spotifyapi().shuffle('true')  
            self.previous_state = 'true'    
            self.name = 'shuffle on'  
            self.show()  
        
class menu_item_refresh(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name, position, page)

    def action(self):
        print('refresh')
        Spotify_API.spotifyapi().refresh()
        
class menu_item_reset(menu_item):
    def __init__(self, name, position, page):
        super().__init__(name, position, page)

    def action(self):
        print('reset')
        Spotify_API.spotifyapi().reset()

class menu_item_ip(menu_item):
    def init(self, name, position, page):
        super().__init__(name, position, page)
    def action(self):
        global active_page
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(str(s.getsockname()[0]))
        
        LCDView.clear_display(LCDView)
        LCDView.print_to_lcd(LCDView,"hostname:"+ hostname,False,1)
        LCDView.print_to_lcd(LCDView,'ip:'+str(s.getsockname()[0]),False,2)

        while True:
            sleep(0.1)
            gpios = [18, 22, 24, 16, 12]
            for gpio in gpios:
                if GPIO.input(gpio) == GPIO.HIGH:
                    print('gpio', gpio, 'pressed')
                    menu_item.show_page(active_page)
                    return
        
class song_handler:
    def check_song():
        playing = ''
        if Spotify_API.spotifyapi().get_currently_playing() != playing:
            if Spotify_API.spotifyapi().get_currently_playing() == 'nothing playing':
                print('nothing playing')
                return 'nothing playing'
            elif Spotify_API.spotifyapi().get_currently_playing() == 'error':
                print('error')
                return 'error'
            else:
                playing = Spotify_API.spotifyapi().get_currently_playing()
                return playing  
           
            



menu.append(menu_item_play('play',1,1))
menu.append(menu_item_pause('pause',2,1))
menu.append(menu_item_shuffle('shuffle',3,1))
menu.append(menu_item_previous('previous',4,1))

menu.append(menu_item_playlist('playlist',1,2))
menu.append(menu_item_devices('devices',2,2))
menu.append(menu_item_refresh('refresh',3,2))
menu.append(menu_item_reset('reset',4,2))

menu.append(menu_item_ip('ip',1,2))

curser = menu_item_curser('curser',0,0)
menu_item.show_page(active_page)


curser = menu_item_curser('curser',0,0)

menu_item.show_page(1)

for item in menu:
    print(item.name)

def down():
    curser.down()
    
def up():
    curser.up()
    
def select():
    menu[curser.position + curser.page].action()

def update():
    global active_page
    menu_item.show_page(active_page)        
        
        
