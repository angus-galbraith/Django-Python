import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
'''(
    QMainWindow,
    QApplication,
    QWidget,
    QStackedLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFont,
)'''

class player:
    def __init__(self,):

        self.name = "Player"
        
        self.stats = {
            "remaining": 501,
            "name": "Player",
            "sets": 0,
            "legs": 0,
            "180": 0,
            "160": 0,
            "140": 0,
            "120": 0,
            "100": 0,
            "80": 0,
            "60": 0,
            "Average": 0,
            "Darts at double": 0,
            "Doubles Hit": 0,
            "Checkout %": 0,
            
        }

class fiveOhOne(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("501")
        self.resize(800,600)
        layout = QGridLayout()
        # player 1
        '''self.legsLabel1 = QLabel("Legs")
        self.legsStats1 = QLabel("1")
        setsLabel1 = QLabel("Sets:")
        layout.addWidget(self.legsLabel1,0,0)
        layout.addWidget(self.legsStats1,0,1)
        layout.addWidget(setsLabel1,1,0)
        #player 2 
        self.legsLabel2 = QLabel("Legs")
        self.legsStats2 = QLabel("1")
        setsLabel2 = QLabel("Sets:")
        layout.addWidget(self.legsLabel2,0,5)
        layout.addWidget(self.legsStats2,0,6)
        layout.addWidget(setsLabel2,1,0)

        # remaing scores and entry box
        self.remaining_label1 = QLabel()
        self.remaining_label1.setFont(QFont("Ariel", 30))
        layout.addWidget(self.remaining_label1, 2, 3)
        self.remaining_label2 = QLabel()
        self.remaining_label2.setFont(QFont("Ariel", 30))
        layout.addWidget(self.remaining_label2, 2, 4)
        self.setLayout(layout)
        self.player1 = player()
        self.player2 = player()
        self.screenRefresh(self.player1)'''
        player1 = player()
        player2 = player()
        player = player1.stats[]
        rownum = 0
        for (key, value) in player.items():
            Label1 = QLabel(key) 
            Label2 = QLabel(value)
            layout.addWidget(Label1,rownum,0)
            layout.addWidget(Label2,rownum,1)
            #tk.Label(frame, text=key).grid(row=rownum, column=0)
            #tk.Label(frame, text=value).grid(row=rownum, column=1)
            rownum += 1

    '''def screenRefresh(self, player):
        self.legsStats1.setText(str(self.player1.stats["legs"]))
        self.legsStats2.setText(str(self.player2.stats["legs"]))

        self.remaining_label1.setText(str(self.player1.stats["remaining"]))
        self.remaining_label2.setText(str(self.player2.stats["remaining"]))'''
         

class roundTheBoard(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Round the board")
        self.resize(800,600)
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
        self.toGoFor = 61
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
        


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.stacklayout = QStackedLayout()
        widget.setLayout(self.stacklayout)
        self.setCentralWidget(widget)

        menu = self.menuBar()

        file_menu = menu.addMenu("Games")
        file_menu2 = menu.addMenu("High Scores")
        #actions
        menu_action = QAction("501", self)
        menu_action2 = QAction("Round the board.", self)
        menu_action3 = QAction("Finishes.", self)

        menu_action4 = QAction("All", self)
        #add actions
        file_menu.addAction(menu_action)
        file_menu.addAction(menu_action2)
        file_menu.addAction(menu_action3)
        file_menu2.addAction(menu_action4)

        #stack the pages 
        darts = fiveOhOne()
        rtb = roundTheBoard()
        finishing = finishes()
        self.stacklayout.addWidget(darts)
        self.stacklayout.addWidget(rtb)
        self.stacklayout.addWidget(finishing)

        menu_action.triggered.connect(self.activate_tab_1)
        menu_action2.triggered.connect(self.activate_tab_2)
        menu_action3.triggered.connect(self.activate_tab_3)


    def activate_tab_1(self):
            self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
            self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
            self.stacklayout.setCurrentIndex(2)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()