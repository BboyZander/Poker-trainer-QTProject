from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

from poker import *
import holdem_calc
import holdem_functions

import numpy as np

class Utils(QtWidgets.QMainWindow):

    def customMessageBox(self, title_text: str, main_text: str, icon_type: str):
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

    def get_odds(self, range, table, hand):
        try:
            board = table # the board equals the flop
            hero_hand = Combo(''.join(hand))
            villan_hand = None # no prior knowledge about the villan
            exact_calculation = False #  calculates exactly by simulating the set of all possible hands
            verbose = True # returns odds of making a certain poker hand, e.g., quads, set, straight
            num_sims = 5 # ignored by exact_calculation = True
            read_from_file = None # we are not reading hands from file

            if range:
                villan_range = Range(range)
                items = [holdem_calc.calculate_odds_villan(board, exact_calculation, 
                                                            num_sims, read_from_file , 
                                                            hero_hand, villan_hand, 
                                                            verbose, print_elapsed_time = False) for villan_hand in villan_range.combos]

                                                

                odds = {}
                [odds.update({odd_type: np.mean([res[0][odd_type] for res in items if res])}) for odd_type in ["tie", "win", "lose"]]


            else:
                odds = holdem_calc.calculate_odds_villan(board, 
                                                exact_calculation, 
                                                num_sims, 
                                                read_from_file , 
                                                hero_hand, 
                                                villan_hand, 
                                                verbose, 
                                                print_elapsed_time = False)
                odds = odds[0]

            print(odds)

        except Exception:
            pass