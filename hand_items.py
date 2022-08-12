from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import pandas as pd

import sys
from poker import Card
from utils import *
import random

class HandItems(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.hand = []

    def hand_cards(self):
        sender = self.sender()
        
        hand = self.hand

        if sender.isChecked():
            hand.append(sender.text())

            for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                if button.text() == sender.text():
                    button.setEnabled(False)

            if len(hand) == 2:
                for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                    if button.text() not in hand:
                        button.setEnabled(False)
        else:
            hand.remove(sender.text())

            for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                if (button.text() == sender.text()) and len(self.table) < 5:
                    button.setEnabled(True)

            if len(hand) < 2:
                for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
                    if button.text() not in self.table:
                        button.setEnabled(True)

        self.get_odds(self.tEdit_range.toPlainText(), self.table, self.hand)

    def clear_hand(self):
        

        for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                button.nextCheckState()

            button.setEnabled(True)

        if len(self.table) < 5:
            for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                if button.text() in self.hand:
                    button.setEnabled(True)

        self.hand = []

    def get_random_hand(self):
        
        hand = self.hand
        dict_suits = {'♠': 's',
                      '♥': 'h',
                      '♦': 'd',
                      '♣': 'c'}

        cards = list(Card)
        cards = [str(i).replace(list(str(i))[1], dict_suits[list(str(i))[1]]) for i in cards]
        if len(self.table) > 0:
            for card in self.table:
                cards.remove(card)
        
        random.shuffle(cards)
        hand = [cards.pop() for __ in range(2)]

        for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
            if button.text() in hand:
                button.setChecked(True)
                button.setEnabled(True)

            else:
                button.setChecked(False)
                button.setEnabled(False)
        
        
        self.hand = hand

        if len(self.table) < 5:
            for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
                if (button.text() in self.hand):
                    button.setEnabled(False)
                else:
                    button.setEnabled(True)

