import sys

from gui.window import MainWindow

from PyQt5.QtWidgets import * 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())