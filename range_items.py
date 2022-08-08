from PyQt6 import QtWidgets

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import re

from poker import Range
from poker.hand import Hand
from utils import *


class RangeItems(QtWidgets.QMainWindow):
    def rangeButtonClicked(self, obj=None):
        """
        Change check status for button and update textEdit, label with combos
        """
        if obj:
            sender = obj
        else:
            sender = self.sender()

        if sender.isChecked():
            new_range = self.tEdit_range.toPlainText() + " " + sender.text()
            self.tEdit_range.setPlainText(str(Range(new_range)))

        else:
            current_range = [
                str(i) for i in Range(self.tEdit_range.toPlainText()).hands
            ]
            new_range = [i for i in current_range if i != sender.text()]
            self.tEdit_range.setPlainText(str(Range(" ".join(new_range))))

        current_range = Range(self.tEdit_range.toPlainText())

        self.update_combo_label(current_range)

    def update_combo_label(self, combos_range):
        """
        Update current number of combos in a Qlabel

        :combos_range: poker Range format of current combos
        """
        sender = self.lbl_cnt_combos

        combos_pattern = "\d* combos"
        percent_pattern = "\d*\.{,1}\d* %"

        combos_text = re.findall(combos_pattern, sender.text())[0]
        percent_text = re.findall(percent_pattern, sender.text())[0]

        new_combos_cnt = 0

        combos = [str(i) for i in combos_range.hands]
        for hand in combos:
            if hand[-1] == "s":
                new_combos_cnt += 4
            elif hand[-1] == "o":
                new_combos_cnt += 12
            else:
                new_combos_cnt += 6

        new_text = (
            sender.text()
            .replace(combos_text, str(new_combos_cnt) + " combos")
            .replace(
                percent_text, str(round(len(combos) / len(list(Hand)) * 100, 1)) + " %"
            )
        )
        sender.setText(new_text)

    def buttons_range(self, button_text):
        """
        Draw range depending on the button
        """
        all_hands = [str(hand) for hand in Range("XX").hands]
        if button_text == "All":
            hands_remained = all_hands

        if button_text == "Broadway":
            hands_remained = [
                hand
                for hand in all_hands
                if (hand[0] in ["A", "K", "Q", "J", "T"])
                and (hand[1] in ["A", "K", "Q", "J", "T"])
            ]

        if button_text == "Pocket":
            hands_remained = [hand for hand in all_hands if len(hand) == 2]

        if button_text == "Suited":
            hands_remained = [hand for hand in all_hands if hand[-1] == "s"]

        range_updated = (
            self.tEdit_range.toPlainText() + " " + str(Range(" ".join(hands_remained)))
        )

        self.tEdit_range.setPlainText(str(Range(range_updated)))

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.text() in hands_remained:
                button.setChecked(True)

        current_range = Range(self.tEdit_range.toPlainText())
        self.update_combo_label(current_range)

    def clear_label(self):
        """
        Change check status of pushed buttons and clear textEdit
        """

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                button.nextCheckState()

        self.tEdit_range.setPlainText("")
        self.tEdit_name.setPlainText("")

        cnt_combos = self.lbl_cnt_combos.text().split()[0]
        self.lbl_cnt_combos.setText(self.lbl_cnt_combos.text().replace(cnt_combos, "0"))

    def tEditTextChangeEvent(self):
        """
        Update all widgets when you change tEdit Plain Text
        """
        text = self.tEdit_range.toPlainText()
        try:
            r_text = Range(text)
            r_text_str = [str(h) for h in r_text.hands]

            for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                if button.text() in r_text_str:
                    button.setChecked(True)
                else:
                    button.setChecked(False)

            self.update_combo_label(r_text)
        except Exception:
            pass
