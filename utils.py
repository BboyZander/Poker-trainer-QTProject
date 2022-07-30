from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

def customMessageBox(title_text: str, main_text: str, icon_type: str):
    msgbox = QMessageBox()
    msgbox.setWindowTitle(title_text)
    msgbox.setText(main_text)
    if icon_type.lower() == 'warning':
        msgbox.setIcon(QMessageBox.Icon.Warning)
    elif icon_type.lower() == 'question':
        msgbox.setIcon(QMessageBox.Icon.Question)
    elif icon_type.lower() == 'information':
        msgbox.setIcon(QMessageBox.Icon.Information)
    else:
        msgbox.setIcon(QMessageBox.Icon.NoIcon)

    msgbox.setStandardButtons(QMessageBox.StandardButton.Ok)
    msgbox.exec()