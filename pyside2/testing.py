#from PySide2.QtGui import QIcon
#from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
#
#app = QApplication([])
#app.setQuitOnLastWindowClosed(False)
#
## Create the icon
#icon = QIcon(r'C:\Users\Tester1\Pictures\icons\icon.png')
#
#def setsystray():# Create the tray
#    tray = QSystemTrayIcon()
#    tray.setIcon(icon)
#    tray.setVisible(True)
#    # Create the menu
#    menu = QMenu()
#    action = QAction("A menu item")
#    menu.addAction(action)
#    # Add a Quit option to the menu.
#    quit = QAction("Quit")
#    quit.triggered.connect(app.quit)
#    menu.addAction(quit)
#    # Add the menu to the tray
#    tray.setContextMenu(menu)
#    
#    app.exec_()
#    
#setsystray()
import pygetwindow as gw  
app = 'Command Prompt'
win2 = gw.getWindowsWithTitle(app)[0]
win2.activate()