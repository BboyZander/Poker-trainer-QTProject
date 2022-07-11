# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pokerRange.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import pandas as pd
from poker import Range


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("pokerRange.ui", self)

        self.add_functions()
        self.dict_range = {}

        self.range_listWidget.installEventFilter(self)
        self.range_listWidget.currentRowChanged.connect(self.display_range_by_item)

        self.tEdit_range.installEventFilter(self)
    
    def add_functions(self):
        """
        Contains all connections between buttons and actions
        """

        self.btn_clear.clicked.connect(self.clear_label)
        self.btn_connect.clicked.connect(self.display_range)

        self.actionLoad.triggered.connect(lambda: self.menu_elements_action(self.actionLoad.text()))
        self.actionSave.triggered.connect(lambda: self.menu_elements_action(self.actionSave.text()))
        self.actionClose.triggered.connect(lambda: self.menu_elements_action(self.actionClose.text()))
        self.btn_saveRange.clicked.connect(self.add_list_widget_item)
        self.btn_delRange.clicked.connect(self.del_item_from_listwidget)
        self.btn_allrange.clicked.connect(lambda: self.buttons_range(self.btn_allrange.text()))
        self.btn_pocket.clicked.connect(lambda: self.buttons_range(self.btn_pocket.text()))
        self.btn_broadway.clicked.connect(lambda: self.buttons_range(self.btn_broadway.text()))
        self.btn_suited.clicked.connect(lambda: self.buttons_range(self.btn_suited.text()))

        self.tEdit_range.textChanged.connect(self.range_by_textedit)


    def eventFilter(self, source, event):
        """
        All keyboard actions
        """
        # right click mouse action for listWidget
        if (event.type() == QtCore.QEvent.ContextMenu and source is self.range_listWidget):
            menu = QtWidgets.QMenu()
            menu.addAction('Open Window')
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                print(item.text())
            return True
        # keyboard enter action for text edit
        if event.type() == QtCore.QEvent.KeyPress and source is self.tEdit_range:
            if event.key() == QtCore.Qt.Key_Return and self.tEdit_range.hasFocus():
                print('Enter pressed')

        return super(Ui_MainWindow, self).eventFilter(source, event)

    def buttons_range(self, button_text):
        """
        Draw range depending on the button
        """
        all_hands = [str(hand) for hand in Range('XX').hands]
        if button_text == 'All':
            hands_remained = all_hands
    
        if button_text == 'Broadway':
            hands_remained = [hand for hand in all_hands if (hand[0] in ['A', 'K', 'Q', 'J', 'T']) and (hand[1] in ['A', 'K', 'Q', 'J', 'T'])]

        if button_text == 'Pocket':
            hands_remained = [hand for hand in all_hands if len(hand) == 2]
 
        if button_text == 'Suited':
            hands_remained = [hand for hand in all_hands if hand[-1] == 's']

        range_updated = self.tEdit_range.toPlainText() + ' ' + str(Range(' '.join(hands_remained)))
        print(range_updated)
        # print(str(Range(' '.join(hands_remained))))

        self.tEdit_range.setPlainText(str(Range(range_updated)))

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.text() in hands_remained:
                button.setChecked(True)

    def range_by_textedit(self):
        text = self.tEdit_range.toPlainText()
        try:
            r_text = Range(text)
            r_text_str = [str(h) for h in r_text.hands]

            for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                if button.text() in r_text_str:
                    button.setChecked(True)
                else:
                    button.setChecked(False)

        except Exception:
            pass

    def menu_elements_action(self, menu_btn):
        """
        Actions for every item in the menu
        """
        if menu_btn == 'Load':
            fname = QFileDialog.getOpenFileName(self, "Open Excel File", "", self.tr("Excel files (*.xlsx *.xls *.xml)"))[0]
            try:
                df = pd.read_excel(fname, dtype={'position': 'str'})
                for k,v in zip(df.position.values, df.range.values):
                    self.dict_range [k] = v

                cnt_current_items = self.range_listWidget.count()
                if cnt_current_items == 0:
                    self.range_listWidget.addItems(df.position.values)
                else: 
                    current_items = [self.range_listWidget.item(i).text() for i in range(self.range_listWidget.count())]
                    want_to_load_items = df.position.values

                    difference = list(set(want_to_load_items) - set(current_items))
                    self.range_listWidget.addItems(difference)


                self.range_listWidget.setCurrentRow(0)

                range_list = [str(hand) for hand in Range(df.range.values[0]).hands]
                for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                    if button.text() in range_list:
                        button.setChecked(True)
                    else:
                        button.setChecked(False)

                
            except FileNotFoundError:
                pass
        
        if menu_btn == 'Save':
            lw = self.range_listWidget
            if lw.count() == 0:
                df = pd.DataFrame({'position': ['current_range'],
                                   'range': [' '.join(self.get_list_of_pushed_buttons()[1].rep_pieces)]})
            else:
                df_form = []
                for i in np.arange(lw.count()):
                    pos_name = lw.item(i).text()
                    range_str = ' '.join(self.dict_range[pos_name].rep_pieces)
                    df_form.append((pos_name, range_str))
                    df = pd.DataFrame(df_form, columns=['position', 'range'])

            fname = QFileDialog.getSaveFileName(self, "Save Excel File", "", self.tr("Excel files (*.xlsx *.xls *.xml)"))[0]

            try:
                df.to_excel(fname, index=False)
            except Exception:
                pass

        if menu_btn == 'Close':
            sys.exit()

    def display_range_by_item(self):
        """
        Connection between QListWidget item and buttons. Display choosen range 
        """
        try:
            pos = self.range_listWidget.currentItem().text()
            range_list = [str(hand) for hand in Range(self.dict_range[pos]).hands]

            for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                    if button.text() in range_list:
                        button.setChecked(True)
                    else:
                        button.setChecked(False)
            
        except AttributeError:
            pass
    
    def clear_label(self):
        """
        Change check status of pushed buttons and clear textEdit
        """

        self.textEdit.setText('')

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                button.nextCheckState()
       
    def get_list_of_pushed_buttons(self):
        """
        Function create list of buttons which Check state is True

        return: list, Range  
        """
        list_of_pushed_button = []

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                list_of_pushed_button.append(button.text())
        range_view_of_pushed_buttons = Range(' '.join(list_of_pushed_button))
        return sorted(list_of_pushed_button), range_view_of_pushed_buttons

    def display_range(self):
        """
        Example of QMessagebox, tmp solution
        """
        _, pos_range = self.get_list_of_pushed_buttons()

        msgbox = QMessageBox()
        msgbox.setWindowTitle('Info')
        msgbox.setText('Вы выбрали следующий диапазон рук')
        msgbox.setIcon(QMessageBox.Information)

        msgbox.setStandardButtons(QMessageBox.Ok)

        msgbox.setInformativeText(', '.join(pos_range.rep_pieces))
        msgbox.setDetailedText(pos_range.to_ascii())
        msgbox.exec_()

    def add_list_widget_item(self):
        """
        Save selected range as an item of QListWidget, also add this information into the dict
        """

        item_name = self.textEdit.toPlainText()
        pos_range = self.get_list_of_pushed_buttons()[1]
        self.dict_range[item_name] = ' '.join(pos_range.rep_pieces)

        if (not self.range_listWidget.findItems(item_name, Qt.MatchExactly)) and (item_name.strip() != ''):
            self.range_listWidget.addItem(item_name)
        else:
            pass
        self.textEdit.setPlainText('')

    def del_item_from_listwidget(self):
        """
        Delete item from QListWidget, also delete it range from the memory
        """
        try:
            item_selected = self.range_listWidget.currentItem()
            del self.dict_range[item_selected.text()]
            self.range_listWidget.takeItem(self.range_listWidget.row(item_selected))
        except AttributeError:
            pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())