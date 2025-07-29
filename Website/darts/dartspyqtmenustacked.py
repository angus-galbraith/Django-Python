from PySide6.QtWidgets import (QApplication, 
QMainWindow, 
QPushButton, 
QLabel, 
QVBoxLayout, QWidget, QMenuBar, QMenu,QHBoxLayout, QStackedLayout, QGridLayout, QLineEdit)
from PySide6.QtGui import QAction
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
        self.resize(600,400)
        self.toGoFor = 1 
        self.runningTotal = 0
        layout = QGridLayout()
        label_togo = QLabel("To go for:")
        label_enter = QLabel("Enter number hit:")
        label_running = QLabel("Running total:")
        self.label_togo_number = QLabel()
        self.label_togo_number.setText(str(self.toGoFor))
        self.label_running_number = QLabel()
        self.label_running_number.setText(str(self.runningTotal))
        self.entry_enter = QLineEdit()
        self.entry_enter.setFixedWidth(30)
        button_enter = QPushButton("Enter")
        button_enter.clicked.connect(self.on_click)
        layout.addWidget(label_togo,0,0)
        layout.addWidget(label_enter,0,1)
        layout.addWidget(label_running,0,2)
        layout.addWidget(self.label_togo_number,1,0)
        layout.addWidget(self.label_running_number,1,2)
        layout.addWidget(self.entry_enter, 1,1)
        layout.addWidget(button_enter, 2,1)
        self.setLayout(layout)

    def on_click(self):
        number_hit = int(self.entry_enter.text())
        temp_score = number_hit * self.toGoFor
        self.runningTotal += temp_score
        self.toGoFor += 1
        self.label_togo_number.setText(str(self.toGoFor))
        self.label_running_number.setText(str(self.runningTotal))
        self.entry_enter.setText("")

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
        self.resize(800,600)
        #Create main widget and insert stacked layout
        widget = QWidget()
        self.stacklayout = QStackedLayout()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)
        
        
    
       

        # setup menus
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.games_menu = QMenu("Games", self)
        self.highscores_menu = QMenu("High Scores", self)
        self.darts_action = QAction("501", self)
        self.rtb_action = QAction("Round the board", self)
        self.finishes_action = QAction("Finishes", self)
        self.allscores_action = QAction("All", self)
        self.games_menu.addAction(self.darts_action)
        self.games_menu.addAction(self.rtb_action)
        self.games_menu.addAction(self.finishes_action)
        self.highscores_menu.addAction(self.allscores_action)
        self.menu_bar.addMenu(self.games_menu) 
        self.menu_bar.addMenu(self.highscores_menu)
        self.darts_action.triggered.connect(self.activate_tab_1)
        self.rtb_action.triggered.connect(self.activate_tab_2)
        self.finishes_action.triggered.connect(self.activate_tab_3)

        rtb = roundTheBoard()
        darts = fiveOhOne()
        finishing = finishes()
        self.stacklayout.addWidget(darts)
        self.stacklayout.addWidget(rtb)
        self.stacklayout.addWidget(finishing)

       
        


    def activate_tab_1(self):
            self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
            self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
            self.stacklayout.setCurrentIndex(2)


    
        

    

    



    






app = QApplication(sys.argv)
#controller = Controller(MainWindow)
w = MainWindow()



w.show()
app.exec()