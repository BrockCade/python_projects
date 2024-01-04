# Import the 'drivers' module to initialize the LCD display
from typing import Any
import drivers

# Initialize the LCD display
display = drivers.Lcd()

# Define a 'LCDView' class for interacting with the LCD display
class LCDView:
    def __init__(self):
        self.curser = '->'  # Define a cursor symbol for highlighting selected options

    # Method to clear a specific line on the LCD display
    def clear_line(self, linenum):
        display.lcd_display_string('                    ', linenum)
    def clear_display(self):
        display.lcd_clear()
    # Method to print text to the LCD display
    def print_to_lcd(self, displaying, clear=True, linenum=1):
        if type(displaying) != str and type(displaying) != list and type(displaying) != dict and type(displaying) != int:
            print('displaying not a string or list',type(displaying))
            return
        # Check if we need to clear the screen
        if clear:
            print('clearing')
            display.lcd_clear()
        elif not clear:
            pass
        else:
            print('clear not a boolean')

        # Check if we are displaying a string or a list
        if type(displaying) == str:
            display.lcd_display_string(displaying, linenum)
        elif type(displaying) == list:
            linenum = 1
            for line in displaying:
                display.lcd_display_string(line, linenum)
                linenum += 1
        elif type(displaying) == dict:
            linenum = 1
            for key in displaying:
                display.lcd_display_string(key, linenum)
                linenum += 1
        elif type(displaying) == int:
            display.lcd_display_string(displaying, linenum)