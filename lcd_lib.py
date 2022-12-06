import board
import digitalio

from time import sleep
wait = 0.001
led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT
led.value = True
rs = digitalio.DigitalInOut(board.GP10)
rw = digitalio.DigitalInOut(board.GP9)
we = digitalio.DigitalInOut(board.GP8)
a0 = digitalio.DigitalInOut(board.GP0)
a1 = digitalio.DigitalInOut(board.GP1)
a2 = digitalio.DigitalInOut(board.GP2)
a3 = digitalio.DigitalInOut(board.GP3)
a4 = digitalio.DigitalInOut(board.GP4)
a5 = digitalio.DigitalInOut(board.GP5)
a6 = digitalio.DigitalInOut(board.GP6)
a7 = digitalio.DigitalInOut(board.GP7)

rw.direction = digitalio.Direction.OUTPUT
rs.direction = digitalio.Direction.OUTPUT
we.direction = digitalio.Direction.OUTPUT
a0.direction = digitalio.Direction.OUTPUT
a1.direction = digitalio.Direction.OUTPUT
a2.direction = digitalio.Direction.OUTPUT
a3.direction = digitalio.Direction.OUTPUT
a4.direction = digitalio.Direction.OUTPUT
a5.direction = digitalio.Direction.OUTPUT
a6.direction = digitalio.Direction.OUTPUT
a7.direction = digitalio.Direction.OUTPUT

letter = []




#

class lcd():
    # setting up the display
    def clear():#clear lcd
        rs.value = False
        a0.value = False
        a1.value = False
        a2.value = False
        a3.value = False
        a4.value = False
        a5.value = False
        a6.value = False
        a7.value = True
        lcd.write()
        
    def home():# homes curser
        rs.value = False
        a0.value = False
        a1.value = False
        a2.value = False
        a3.value = False
        a4.value = False
        a5.value = False
        a6.value = True
        a7.value = False
        lcd.write()
    class curser():
        def curser(direction):#sets direction of cureser left or right i think ?
            rs.value = False
            a0.value = False
            a1.value = False
            a2.value = False
            a3.value = True
            a4.value = False
            a5.value = False
            if direction == 'left':
                a4.value = False
                a5.value = False
            elif direction == 'right':
                a4.value = False
                a5.value = True
            else:
                print('unknown direction direction should be left or right')
            a6.value = False
            a7.value = False
            lcd.write()
            
        def blink(value):
            rs.value = False
            a0.value = False
            a1.value = False
            a2.value = False
            a3.value = False
            a4.value = True
            a5.value = True
            a6.value = False
            if value == 'on':
                print('51')
                a7.value = True
            elif value == 'off':
                print('52')
                a7.value = False
            else:
                print('55')
    def setup():#sets lcd to 8 bit mode number of linse to 2 and font type is set to 5 x 11
        rs.value = False
        a0.value = False
        a1.value = False
        a2.value = False
        a3.value = False
        a4.value = True
        a5.value = True
        a6.value = False
        a7.value = True
        lcd.write()
     
        
    class display():#turns display on
        def on():
            rs.value = False
            a0.value = False
            a1.value = False
            a2.value = False
            a3.value = False
            a4.value = True
            a5.value = True
            a6.value = False
            a7.value = True
            lcd.write()
    
        def off():#turns display off
            rs.value = False
            a0.value = False
            a1.value = False
            a2.value = False
            a3.value = False
            a4.value = False
            a5.value = True
            a6.value = False
            a7.value = True
            lcd.write()
     
    def str_to_bin(data):
        string = data
        lst = []
        lst2 = []
        mystring  = ''
        #convert str to list of charaters
        for letter in string:
            lst.append(letter)
        #converts list of charaters to list of dec
        for letters in lst:
            lst2.append(ord(letters))
        
        lst.clear()
        #converts the list of dec to a list str os dec
        lst = [str(x) for x in lst2]
        
        lst2.clear()
        #converst the list of dec to bin
        for dec in lst:
            lst2.append(bin(int(dec))[2:])
    
        lst.clear()
        #formats the bin so giveing it 0s to make it 8 long
        for things in lst2:
            if len(things) != 8:
                numof = abs(len(things) - 8)
                if numof == 1:
                    long8 = '0' + things
                    lst.append(long8)
                elif numof == 2:
                    long8 = '0' + '0' + things
                    lst.append(long8)
        
        lst2.clear()
        #converst list to string
        for x in lst:
            mystring += '' + x
        
        #converts string to list
        for chat in mystring:
            lst2.append(chat)
        lst.clear()
        
        #converts string to list
        lst = [eval(i) for i in lst2]
       
        return lst
        
    def write_data(list):
        counter = 0
        loop = 0
        try:
            while True:
                rs.value = 1
                a0.value = list[0 + counter]
                a1.value = list[1 + counter]
                a2.value = list[2 + counter]
                a3.value = list[3 + counter]
                a4.value = list[4 + counter]
                a5.value = list[5 + counter]
                a6.value = list[6 + counter]
                a7.value = list[7 + counter]
                loop = loop + 1
                counter = counter + 8
                if loop == 1:
                    #print('write')
                    loop = loop - 1
                    lcd.write()
                    #lcd.display.on()
        except:
            pass
    def send(string):
        bin_data = lcd.str_to_bin(string)
        lcd.write_data(bin_data)
       
    
            
    def data():
         rs.value = 1
         a0.value = False
         a1.value = True
         a2.value = True
         a3.value = False
         a4.value = True
         a5.value = False
         a6.value = False
         a7.value = False
         lcd.write()
    def data3():
         rs.value = 1
         a0.value = 0
         a1.value = 0
         a2.value = 1
         a3.value = 0
         a4.value = 0
         a5.value = 1
         a6.value = 0
         a7.value = 1
         lcd.write()
         
            
    def write():#turns we on to wright the data
        sleep(wait)
        we.value = True
        sleep(wait)
        we.value = False
        

    
lcd.clear()
lcd.curser.blink('off')
lcd.home()
lcd.setup()

    






