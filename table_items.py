from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import numpy as np
import pandas as pd

from utils import *

class TableItems(QtWidgets.QMainWindow):

    def tc(self):
        sender = self.sender()
        if sender.isChecked():
            print(sender.text())