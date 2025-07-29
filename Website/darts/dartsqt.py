from PyQt5.QtWidgets import (QApplication, 
QMainWindow, 
QPushButton, 
QLabel, 
QVBoxLayout, QWidget, QMenuBar, QMenu, QAction,QHBoxLayout, QStackedLayout)

import sys

from random import randint


class fiveOhOne(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("501")
        self.resize(800,600)
        layout = QVBoxLayout()
        self.label = QLabel("501 ")
        layout.addWidget(self.label)
        self.setLayout(layout)


class roundTheBoard(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Round the board")
        self.resize(800,600)
        layout = QVBoxLayout()
        self.label = QLabel("Round the board")
        
        layout.addWidget(self.label)
        self.setLayout(layout)

class finishes(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finishes")
        self.resize(800,600)
        layout = QVBoxLayout()
        self.label = QLabel("Finishes")
        
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main window")
        self.resize(1000,600)
        widget = QWidget()
        layout2 = QHBoxLayout()
        self.label = QLabel("Main window")
        self.label2 = QLabel("bob")
        name = "Gus"
        self.label2.setText(name)
        layout2.addWidget(self.label)
        layout2.addWidget(self.label2)
        widget.setLayout(layout2)
        self.setCentralWidget(widget)
        
        
    
       

        # setup menus
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.games_menu = QMenu("Games", self)
        self.darts_action = QAction("501", self)
        self.rtb_action = QAction("Round the board", self)
        self.finishes_action = QAction("Finishes", self)
        self.games_menu.addAction(self.darts_action)
        self.games_menu.addAction(self.rtb_action)
        self.games_menu.addAction(self.finishes_action)
        self.menu_bar.addMenu(self.games_menu) 
        self.darts_action.triggered.connect(controller.show_window2)
        self.rtb_action.triggered.connect(controller.show_window3)
        self.finishes_action.triggered.connect(controller.show_window4)

       
        


    
        

    

    



    


class Controller:

    def __init__(self, window):
        self.window = window
        self.window2 = fiveOhOne()
        self.window3 = roundTheBoard()
        self.window4 = finishes()

    def hide_all_windows(self):
        self.window2.hide()
        self.window3.hide()
        self.window4.hide()

        
    def show_window2(self):
        self.hide_all_windows()
        self.window2.show()

    def show_window3(self):
        self.hide_all_windows()
        self.window3.show()
        

    def show_window4(self):
        self.hide_all_windows()
        self.window4.show()   
        



app = QApplication(sys.argv)
controller = Controller(MainWindow)
w = MainWindow()



w.show()
app.exec()