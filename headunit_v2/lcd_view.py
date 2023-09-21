import drivers
# Initialize the LCD display
display = drivers.Lcd()


class LCDView:
    def __init__(self):
        self.curser = '->'

    def clear_line(self,linenum):
        display.lcd_display_string('                    ', linenum)

    def print_to_lcd(self,displaying,clear = True,linenum = 1):
            #check if we need to clear the screen
            if clear == True:
                print('clearing')
                display.lcd_clear()
            elif clear == False:
                pass
            else:
                print('clear not a boolean')

            #check if we are displaying a string or a list
            if type(displaying) == str:
                #print('displaying: ' + displaying)
                display.lcd_display_string(displaying, linenum)
            elif type(displaying) == list:
                linenum = 1
                for line in displaying:
                    display.lcd_display_string(line, linenum)
                    linenum = linenum + 1
            else:
                print('displaying not a string or list')


class view_logic(LCDView):
    def __init__(self):
        super().__init__()
        pass
        #self.print_to_lcd(self.curser + self.page1[0],False,1)

    def display_menu(self,curser_position,page,clear = False,previus_position = 1):
        print(page)
        self.clear_line(previus_position)
        self.menu_refresh(page)
        self.print_to_lcd(self.curser + page[curser_position - 1],clear,curser_position)
    
    def menu_refresh(self,page):
        for item in page:
            self.print_to_lcd(item,False,page.index(item) + 1)


