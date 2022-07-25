# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pokerRange.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from select import select
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox, QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

# from PySide2.QtWidgets import *
# from PySide2.QtCore import Qt

import numpy as np
import pandas as pd
import math
import re

from poker import Range
from poker.hand import Hand

from windowClasses import ExtraWindow_label


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("pokerRange.ui", self)

        self.buttons_click_actions()
        self.dict_range = {}

        self.eventfilter_elements()

        self.range_listWidget.installEventFilter(self)
        self.range_listWidget.currentRowChanged.connect(self.display_range_by_item)



    def eventfilter_elements(self):
        """
        Contains all elements which uses alternative event filter
        """

        self.lbl_cnt_combos.installEventFilter(self)

    
    def buttons_click_actions(self):
        """
        Contains all connections between buttons and actions
        """
        self.btn_connect.clicked.connect(self.display_range)

        self.actionLoad.triggered.connect(lambda: self.menu_elements_action(self.actionLoad.text()))
        self.actionSave.triggered.connect(lambda: self.menu_elements_action(self.actionSave.text()))
        self.actionClose.triggered.connect(lambda: self.menu_elements_action(self.actionClose.text()))

        self.btn_allrange.clicked.connect(lambda: self.buttons_range(self.btn_allrange.text()))
        self.btn_pocket.clicked.connect(lambda: self.buttons_range(self.btn_pocket.text()))
        self.btn_broadway.clicked.connect(lambda: self.buttons_range(self.btn_broadway.text()))
        self.btn_suited.clicked.connect(lambda: self.buttons_range(self.btn_suited.text()))
        self.btn_clear.clicked.connect(self.clear_label)

        self.tEdit_range.textChanged.connect(self.tEditTextChangeEvent)

        self.checkBox_hoverMode.stateChanged.connect(self.Hover_method)

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            button.clicked.connect(lambda: self.rangeButtonClicked())

        self.btn_addRange.clicked.connect(lambda: self.treeWidget_buttons(self.btn_addRange.text()))
        self.btn_Delete.clicked.connect(lambda: self.treeWidget_buttons(self.btn_Delete.text()))
        self.btn_addCategory.clicked.connect(lambda: self.treeWidget_buttons(self.btn_addCategory.text()))
        self.btn_Rename.clicked.connect(lambda: self.treeWidget_buttons(self.btn_Rename.text()))






    def eventFilter(self, obj, event):
        """
        Contains custom events
        """
        if event.type() == QEvent.Type.HoverEnter:
            sender = obj
            if type(sender) == QtWidgets.QPushButton:
                sender.nextCheckState()
                self.rangeButtonClicked(sender)

        if event.type() == QEvent.Type.MouseButtonDblClick and obj is self.lbl_cnt_combos:
            ui = ExtraWindow_label(self)
            ui.show()



        elif event.type() == QEvent.Type.HoverMove:
            pass
        elif event.type() == QEvent.Type.HoverLeave:
            pass
        return super().eventFilter(obj, event)

    def Hover_method(self):
        """
        Activate hover mode for range buttons
        """
        sender = self.sender()
        if sender.isChecked():
            for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                button.setAttribute(Qt.WidgetAttribute.WA_Hover)
                button.installEventFilter(self)
        else:
            for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
                button.removeEventFilter(self)

    def rangeButtonClicked(self, obj = None):
        """
        Change check status for button and update textEdit, label with combos 
        """
        if obj:
            sender = obj
        else:
            sender = self.sender()

        if sender.isChecked():
            new_range = self.tEdit_range.toPlainText() + ' ' + sender.text()
            self.tEdit_range.setPlainText(str(Range(new_range)))
        
        else:
            current_range = [str(i) for i in Range(self.tEdit_range.toPlainText()).hands]
            new_range = [i for i in current_range if i != sender.text()]
            self.tEdit_range.setPlainText(str(Range(' '.join(new_range))))

        current_range = Range(self.tEdit_range.toPlainText())
        
        self.update_combo_label(current_range)


    def update_combo_label(self, combos_range):
        """
        Update current number of combos in a Qlabel

        :combos_range: poker Range format of current combos
        """
        sender = self.lbl_cnt_combos

        combos_pattern = '\d* combos'
        percent_pattern = '\d*\.{,1}\d* %'
        
        combos_text = re.findall(combos_pattern, sender.text())[0]
        percent_text = re.findall(percent_pattern, sender.text())[0]

        new_combos_cnt = 0

        combos = [str(i) for i in combos_range.hands]
        for hand in combos:
            if hand[-1] == 's':
                new_combos_cnt += 4
            elif hand[-1] == 'o':
                new_combos_cnt += 12
            else:
                new_combos_cnt += 6
        
        new_text = sender.text().replace(combos_text, str(new_combos_cnt) + ' combos').replace(percent_text, str(round(len(combos)/ len(list(Hand))* 100, 1)) + ' %')
        sender.setText(new_text)    

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

        self.tEdit_range.setPlainText(str(Range(range_updated)))

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.text() in hands_remained:
                button.setChecked(True)

        current_range = Range(self.tEdit_range.toPlainText())
        self.update_combo_label(current_range) 

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

                self.statusBar().showMessage('Range loaded')    
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
                self.statusBar().showMessage('Range saved') 
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

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                button.nextCheckState()

        self.tEdit_range.setPlainText('')
        cnt_combos = self.lbl_cnt_combos.text().split()[0]
        self.lbl_cnt_combos.setText(self.lbl_cnt_combos.text().replace(cnt_combos, '0'))
       
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

    # TODO: запретить вложенность дальше второго уровня при добавлении рейнджа
    def treeWidget_buttons(self, btn_name):
        
        widget = self.treeWidget_range

        if btn_name == 'Add Range':

            current_item = widget.currentItem()
            category_name = self.textEdit_name.toPlainText()

            if category_name == '':
                name = str(current_item.childCount())
            else:
                name = category_name

            childWidget = QtWidgets.QTreeWidgetItem(current_item)
            childWidget.setText(0, name)
            current_item.addChild(childWidget)




            
            print('cur item: ', widget.currentItem())

            print('btn_addRange clicked')

        elif btn_name == 'Add Category':
            current_top_lvl_items = [widget.topLevelItem(i).text(0) for i in range(widget.topLevelItemCount())]

            category_name = self.textEdit_name.toPlainText()
            if category_name == '':
                name = str(widget.topLevelItemCount())
            else:
                name = category_name

            if name not in current_top_lvl_items:
                widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([name]))

        elif btn_name == 'Rename':
            selected_item = widget.currentItem()
            
            category_name = self.textEdit_name.toPlainText()
            if category_name == '':
                name = 'error'
            else:
                name = category_name

            selected_item.setText(0, name)
            

            print('btn_Rename clicked')

        elif btn_name == 'Delete':
            try:
                selected_item = widget.currentItem()
                parent = selected_item.parent()

                if parent:
                   parent.takeChild(parent.indexOfChild(selected_item))
                else:
                    index = widget.indexOfTopLevelItem(selected_item)
                    widget.takeTopLevelItem(index)
            except Exception:
                pass

            print('btn_Delete clicked')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec())