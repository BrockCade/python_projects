from lcd_lib import *
from time import sleep
from adafruit_matrixkeypad import *
from digitalio import DigitalInOut
import board
lcd.send('loadingO_O')
counter23 = 0
while counter23 < 5:
    lcd.curser.blink('off')
    
    sleep(0.5)
    lcd.curser.curser('left')
    lcd.send('-')
    sleep(0.5)
    lcd.curser.curser('left')
    lcd.send('O')
    counter23 = counter23 + 1
lcd.clear()


def add(number1,number2):
    answer = (number1 + number2)
    return answer
def subtract(number1,number2):
    answer = (number1 - number2)
    return answer
def multiply(number1,number2):
    answer = (number1 * number2)
    return answer
def divide(number1,number2):
    try:
        answer = (number1 / number2)
        return answer
    except Exception as e:
        lcd.send(str(e))
        
    

def solve(user,user2,operation):
    if operation == '+':
        answer = add(user,user2)
    elif operation == '-':
        answer = subtract(user,user2)
    elif operation == '*':
        answer = multiply(user,user2)
    elif operation == '/':
        print(user,user2)
        answer = divide(user,user2)
        
    print(answer)
    lcd.send(' = ')
    lcd.send(str(answer))
#data = user_input()
#solve(*data)





# Classic 3x4 matrix keypad
cols = [DigitalInOut(x) for x in (board.GP20, board.GP21, board.GP22, board.GP26)]
rows = [DigitalInOut(x) for x in (board.GP16, board.GP17, board.GP18, board.GP19)]
keys = ((1, 2, 3, '+'),
        (4, 5, 6, '-'),
        (7, 8, 9, '*'),
        ('c', 0, '=', '/'))

keypad = Matrix_Keypad(rows, cols, keys)
op = ['+','-','*','/','=','c']
op2 = ['=','c']
counter = 0
user = ''
user2 = ''
st = ''
st2 = ''
while True:
    
    keys = keypad.pressed_keys
    if keys:
        st = (str(keys))
        st2 = st.strip(']').strip('[').strip("'")
        print(type(st2))
        if all(st2 != item for item in op):
            if counter == 0:
                print('1')
                user = user + st2
                print(user)
                lcd.send(str(st2))
            if counter == 1:
                print('2')
                user2 = user2 + st2
                lcd.send(str(st2))
                print(user2)
        elif all(st2 != item for item in op2):
            print('3')
            operation = st2
            lcd.send(str(operation))
            counter = counter + 1
        elif st2 == 'c':
            lcd.clear()
            counter = 0
            user = ''
            user2 = ''
            st = ''
            st2 = ''
        else:
            print('4')
            solve(int(user),int(user2),operation)
            counter = 0
            user = ''
            user2 = ''
            st = ''
            st2 = ''
            
        
    sleep(0.3)