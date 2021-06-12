import interface
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Windows')
    ex = interface.AppWindow()
    sys.exit(app.exec_())
