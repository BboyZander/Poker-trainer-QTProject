from PyQt6 import QtWidgets, uic

from PyQt6.QtCore import *
from PyQt6.QtGui import *

from poker import Range
from poker.hand import Hand

import sys
import os

from range_package import hand_items,table_items, range_items, tree_widget_items
import utils

class Trainer_window(  
    tree_widget_items.TreeWidgetItems,  
    utils.Utils,
    QtWidgets.QMainWindow,
):
    def __init__(self, parent=None):
        super(Trainer_window, self).__init__(parent)
        uic.loadUi("window_trainer.ui", self)

        self.setFixedHeight(670)
        self.setFixedWidth(1110)


#just for testing
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Trainer_window()
    ui.show()
    sys.exit(app.exec())