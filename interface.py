from PyQt5.QtWidgets import (QWidget, QTextEdit, QGridLayout, QApplication,
    QMenu, QDesktopWidget, QMenuBar, QMainWindow, QVBoxLayout, QLabel, QTableWidget,
    QAction, QGridLayout, QTabWidget, QPushButton, QLabel, QLineEdit)
from PyQt5.QtGui import QIcon

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(900, 563)
        self.center()
        self.setWindowTitle('Magic: The Gathering')
        self.setWindowIcon(QIcon('icon.png'))

        self.connectAction =  QAction(QIcon("connect.png"), "Connect database...", self)
        self.dropAction =  QAction(QIcon("drop.png"), "Drop database...", self)
        self.deleteStringAction =  QAction("Delete String...", self)
        self.deleteTableAction = QAction("Delete Table...", self)
        self.deleteAllAction = QAction("Delete All...", self)
        self.menuBar = QMenuBar()
        self.menu = self.menuBar.addMenu(QIcon("menu.png"), "Menu")
        self.menu.addAction(self.connectAction)
        self.menu.addAction(self.dropAction)
        self.menu.addSeparator()
        self.miniMenu = self.menu.addMenu(QIcon("delete.png"), "Delete...")
        self.miniMenu.addAction(self.deleteStringAction)
        self.miniMenu.addAction(self.deleteTableAction)
        self.miniMenu.addAction(self.deleteAllAction)
        self.setMenuBar(self.menuBar)

        self.tab_widget = MyTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class MyTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QGridLayout()
        self.tabs = QTabWidget()
        self.cardsTab = QWidget()
        self.shopsTab = QWidget()
        self.tabs.addTab(self.cardsTab,"Cards")
        self.tabs.addTab(self.shopsTab,"Shops")

        self.cardsTab.layout = QGridLayout()
        self.nameLabel = QLabel('Name:')
        self.setLabel = QLabel('Set:')
        self.keyLabel = QLabel('Key name:')
        self.nameEdit = QLineEdit()
        self.setEdit = QLineEdit()
        self.keyEdit = QLineEdit()
        self.addButton = QPushButton("add")
        self.deleteButton = QPushButton("delete")
        self.searchButton = QPushButton("search")
        self.cardWidget = QTableWidget(self.cardsTab)
        self.cardWidget.setColumnCount(4)
        self.cardWidget.setHorizontalHeaderLabels(["id", "Image", "Name", "Set"])
        self.cardsTab.layout.addWidget(self.nameLabel, 1, 0)
        self.cardsTab.layout.addWidget(self.nameEdit, 1, 1)
        self.cardsTab.layout.addWidget(self.setLabel, 2, 0)
        self.cardsTab.layout.addWidget(self.setEdit, 2, 1)
        self.cardsTab.layout.addWidget(self.addButton, 3, 1)
        self.cardsTab.layout.addWidget(self.keyLabel, 1, 3)
        self.cardsTab.layout.addWidget(self.keyEdit, 1, 4)
        self.cardsTab.layout.addWidget(self.deleteButton, 2, 4)
        self.cardsTab.layout.addWidget(self.searchButton, 3, 4)
        self.cardsTab.layout.addWidget(self.cardWidget, 4, 0, 9, 0)

        self.shopsTab.layout = QGridLayout()
        self.shopLabel = QLabel('Shop:')
        self.setLabel_ = QLabel('Set:')
        self.costLabel = QLabel('Cost:')
        self.keyLabel_ = QLabel('Key name:')
        self.shopEdit = QLineEdit()
        self.setEdit_ = QLineEdit()
        self.costEdit = QLineEdit()
        self.keyEdit_ = QLineEdit()
        self.addButton_ = QPushButton("add")
        self.deleteButton_ = QPushButton("delete")
        self.searchButton_ = QPushButton("search")
        self.shopWidget = QTableWidget(self.shopsTab)
        self.shopWidget.setColumnCount(6)
        self.shopWidget.setHorizontalHeaderLabels(["id", "Set", "Shop", "Cost", "Creation time", "Last modified"])
        self.shopsTab.layout.addWidget(self.setLabel_, 1, 0)
        self.shopsTab.layout.addWidget(self.setEdit_, 1, 1)
        self.shopsTab.layout.addWidget(self.shopLabel, 2, 0)
        self.shopsTab.layout.addWidget(self.shopEdit, 2, 1)
        self.shopsTab.layout.addWidget(self.costLabel, 3, 0)
        self.shopsTab.layout.addWidget(self.costEdit, 3, 1)
        self.shopsTab.layout.addWidget(self.addButton_, 4, 1)
        self.shopsTab.layout.addWidget(self.keyLabel_, 1, 3)
        self.shopsTab.layout.addWidget(self.keyEdit_, 1, 4)
        self.shopsTab.layout.addWidget(self.deleteButton_, 2, 4)
        self.shopsTab.layout.addWidget(self.searchButton_, 3, 4)
        self.shopsTab.layout.addWidget(self.shopWidget, 5, 0, 9, 0)
            
        self.cardsTab.setLayout(self.cardsTab.layout)
        self.shopsTab.setLayout(self.shopsTab.layout)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)    
