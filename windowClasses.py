from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import sys

class ExtraWindow_label(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(ExtraWindow_label, self).__init__(parent)
        uic.loadUi("extraWindow_label.ui", self)

        self.btn_CANCEL.clicked.connect(self.close_window)
        

    def close_window(self):
        self.close()

#just for testing
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = ExtraWindow_label()
    ui.show()
    sys.exit(app.exec())
