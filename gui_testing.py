from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox,QApplication, QSystemTrayIcon, QMenu, QAction
import sys,time
from PySide2.QtGui import QIcon
location = r'C:\Users\Tester1\Pictures\icons\icon.png'
class Window(QWidget): 
    def __init__(self):
        super().__init__()
        
        #initiates things
        self.setWindowTitle("window1")
        self.setGeometry(300,300,300,300)
        self.setIcon()
        self.setButton()
        
        
            
    def setIcon(self):
        appIcon = QIcon(location)
        self.setWindowIcon(appIcon)
    #setup/logic for button        
    def setButton(self):
        btn1 = QPushButton("quit",self)
        btn1.clicked.connect(self.quitApp)
        
    def quitApp(self):
        userInfo = QMessageBox.question(self,"confirmation","Are you sure you want to quit!!",QMessageBox.Yes|QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            window.hide()
        elif userInfo == QMessageBox.No:
            pass
        else:
            pass
        
        
class systray(QWidget): 
    def __init__(self):
        super().__init__()
        def do():
            print("hi")
        icon = QIcon(r'C:\Users\Tester1\Pictures\icons\icon.png')
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        # Create the menu
        menu = QMenu()
        action = QAction("A menu item")
        menu.addAction(action)
        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(myapp.quit)
        menu.addAction(quit)
        # Add the menu to the tray
        tray.setContextMenu(menu) 
        #activate on L click
        tray.activated.connect(window.show)
        #activate on menu element being clicked
        menu.triggered.connect(do)
        #activate just before menu show up
        menu.aboutToShow.connect(do)
        myapp.exec_()
   
myapp = QApplication(sys.argv)
window = Window()
systray()


sys.exit()