from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import numpy as np
import pandas as pd
import math
import re
import json

from poker import Range
from poker.hand import Hand
from utils import *

def table_cards(button):
    sender = button
    if sender.isChecked():
        print(sender.text())