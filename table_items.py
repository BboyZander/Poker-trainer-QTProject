from string import capwords
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import numpy as np
import pandas as pd

from utils import *
import random
import poker


class TableItems(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = []


    def table_cards(self):
        """
        Table buttons events
        """
        sender = self.sender()
        
        deck = self.table


        if sender.isChecked():
            deck.append(sender.text())

            if len(self.dict_table["Flop"]) < 3:
                self.dict_table["Flop"].append(sender.text())
                if self.tEditFlop1.toPlainText() == '':
                    self.tEditFlop1.setPlainText(sender.text())
                elif self.tEditFlop2.toPlainText() == '':
                    self.tEditFlop2.setPlainText(sender.text())
                else:
                    self.tEditFlop3.setPlainText(sender.text())
            elif len(self.dict_table["Turn"]) < 1:
                self.dict_table["Turn"].append(sender.text())
                self.tEditTurn.setPlainText(sender.text())

                sender.setIcon(QIcon('pictures/T.png'))
                sender.setIconSize(QSize(8,8))
            elif len(self.dict_table["River"]) < 1:
                self.dict_table["River"].append(sender.text())
                self.tEditRiver.setPlainText(sender.text())
                
                sender.setIcon(QIcon('pictures/R.png'))
                sender.setIconSize(QSize(8,8))

            if len(deck) == 5:
                for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                    if button.text() not in deck:
                        button.setEnabled(False)
            
            for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                if button.text() == sender.text():
                    button.setEnabled(False)

        else:
            deck.remove(sender.text())
            sender.setIcon(QIcon())
            if len(deck) < 5:
                for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                    if button.text() not in self.hand:
                        button.setEnabled(True)


            for key in self.dict_table.keys():
                try:
                    self.dict_table[key].remove(sender.text())
                except ValueError:
                    pass
            
            if self.tEditFlop1.toPlainText() == sender.text():
                self.tEditFlop1.setPlainText('')
            elif self.tEditFlop2.toPlainText() == sender.text():
                self.tEditFlop2.setPlainText('')
            elif self.tEditFlop3.toPlainText() == sender.text():
                self.tEditFlop3.setPlainText('')
            elif self.tEditTurn.toPlainText() == sender.text():
                self.tEditTurn.setPlainText('')
            else:
                self.tEditRiver.setPlainText('')

            for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                if (button.text() == sender.text()) and len(self.hand) < 2:
                    button.setEnabled(True)

        self.table = deck

    def clear_table(self):
        """
        Clear table items
        """


        for key in self.dict_table.keys():
            self.dict_table[key] = []

        for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                button.nextCheckState()
                button.setIcon(QIcon())


            button.setEnabled(True)
        
        self.tEditFlop1.setPlainText('')
        self.tEditFlop2.setPlainText('')
        self.tEditFlop3.setPlainText('')
        self.tEditTurn.setPlainText('')
        self.tEditRiver.setPlainText('')
        
        if len(self.hand) < 2:
            for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                if button.text() in self.table:
                    button.setEnabled(True)

        self.table = []

    def get_random_table(self):
        """
        Generate random table
        """
        deck = self.table
        dict_suits = {'♠': 's',
                      '♥': 'h',
                      '♦': 'd',
                      '♣': 'c'}

        cards = list(poker.Card)
        cards = [str(i).replace(list(str(i))[1], dict_suits[list(str(i))[1]]) for i in cards]
        if len(self.hand) > 0:
            for card in self.hand:
                cards.remove(card)
        random.shuffle(cards)
        deck = [cards.pop() for __ in range(5)]

        self.dict_table['Flop'] = deck[:3]
        self.dict_table['Turn'] = [deck[3]]
        self.dict_table['River'] = [deck[4]]

        for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
            if button.text() in deck:
                if button.text() == deck[3]:
                    button.setIcon(QIcon('pictures/T.png'))
                    button.setIconSize(QSize(8,8))
                
                if button.text() == deck[4]:
                    button.setIcon(QIcon('pictures/R.png'))
                    button.setIconSize(QSize(8,8))

                button.setChecked(True)
                button.setEnabled(True)

            else:
                button.setChecked(False)
                button.setEnabled(False)
                button.setIcon(QIcon())

        self.tEditFlop1.setPlainText(deck[0])
        self.tEditFlop2.setPlainText(deck[1])
        self.tEditFlop3.setPlainText(deck[2])
        self.tEditTurn.setPlainText(deck[3])
        self.tEditRiver.setPlainText(deck[4])

        self.table = deck

        if len(self.hand) < 2:
            for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                if (button.text() in self.table):
                    button.setEnabled(False)
                else:
                    button.setEnabled(True)
