import sys

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
    QGridLayout,
    QLineEdit,
)

from layout_colorwidget import Color

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
        self.label_togo = QLabel("To go for:")
        layout.addWidget(self.label_togo, 0,0)
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

        self.setWindowTitle("My App")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        rtb = roundTheBoard()
        self.stacklayout.addWidget(rtb)

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

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
