import Spotify_API
import time
spotifyapi = Spotify_API.spotifyapi
global curser_position
curser_position = 1
global page
page = 0

pages = {
            'play_menu': ['play', 'pause', 'skip','previous' ],
            'settings': ['settings', '...','...','refresh'],
        }
keys = list(pages.keys())

class curser:
    def __init__(self):
        pass
          
    def start(self):
        global curser_position
        global page
        return curser_position,pages[keys[page]]
     
    def curser_direction(self,diraction):
        global curser_position
        global page
        previus_position = curser_position
        clear = False

        if diraction == 'up':
            curser_position = curser_position - 1
            if curser_position == 0:
                curser_position = 1
                if page != 0:
                    page = page - 1
                    #clear = True
            print('up',curser_position)
            print('page',page)

        elif diraction == 'down':
            curser_position = curser_position + 1
            if curser_position == 5:
                curser_position = 1
                print(type(len(keys)))
                if page != len(keys) -1:
                    page = page + 1
                    #clear = True
            print('down',curser_position)
            print('page',page)

        elif diraction == 'left':
            spotifyapi().previous()
            return 
        elif diraction == 'right':
            spotifyapi().skip()
            return
        
        return curser_position,pages[keys[page]],clear,previus_position
    
    def selecter(self):
        spotifyapi().pick(pages[keys[page]][curser_position - 1])

    
class timer():
    def __init__(self):
        self.starttime = None
       

    def start(self):
        self.starttime = time.perf_counter()

    def stop(self):
        self.endtime = time.perf_counter() - self.starttime
        print(f"{self.endtime:0.4f}")
        return self.endtime
   

        
class song_handler():
    def check_song():
        playing = ''
        if spotifyapi().get_currently_playing() != playing:
            if spotifyapi().get_currently_playing() == 'nothing playing':
                print('nothing playing')
                return 'nothing playing'
            elif spotifyapi().get_currently_playing() == 'error':
                print('error')
                return 'error'
            else:
                playing = spotifyapi().get_currently_playing()
                print(playing)
                return playing
