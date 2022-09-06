from PyQt6 import QtWidgets, uic

from PyQt6.QtCore import *
from PyQt6.QtGui import *

from poker import Range
from poker.hand import Hand

from windowClasses import ExtraWindow_label
import table_items, top_menu, range_items, tree_widget_items, hand_items, utils


class Ui_MainWindow(
    tree_widget_items.TreeWidgetItems,
    range_items.RangeItems,
    table_items.TableItems,
    top_menu.TopMenu,
    hand_items.HandItems,
    utils.Utils,
    QtWidgets.QMainWindow,
):
    def __init__(self):
        super().__init__()
        uic.loadUi("pokerRange.ui", self)

        self.dict_range = {}
        self.dict_table = {"Flop": [], "Turn": [], "River": []}

        self.tree_item_actions()
        self.range_item_actions()
        self.table_item_actions()
        self.hand_item_actions()
        
        self.buttons_click_actions()

        self.eventfilter_elements()

        # self.treeWidget_range.itemDoubleClicked.connect(self.rename_value)
        # self.treeWidget_range.itemChanged.connect(self.checkName, Qt.ConnectionType.QueuedConnection)

    def eventfilter_elements(self):
        """
        Contains all elements which uses alternative event filter
        """

        self.lbl_cnt_combos.installEventFilter(self)

    def tree_item_actions(self):

        self.treeWidget_range.itemClicked.connect(self.display_range_by_item)

        self.btn_addRange.clicked.connect(
            lambda: self.treeWidget_buttons(self.btn_addRange.text())
        )
        self.btn_Delete.clicked.connect(
            lambda: self.treeWidget_buttons(self.btn_Delete.text())
        )
        self.btn_addCategory.clicked.connect(
            lambda: self.treeWidget_buttons(self.btn_addCategory.text())
        )
        self.btn_Rename.clicked.connect(
            lambda: self.treeWidget_buttons(self.btn_Rename.text())
        )

    def range_item_actions(self):
        
        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            button.clicked.connect(lambda: self.rangeButtonClicked())

        self.btn_allrange.clicked.connect(
            lambda: self.buttons_range(self.btn_allrange.text())
        )
        self.btn_pocket.clicked.connect(
            lambda: self.buttons_range(self.btn_pocket.text())
        )
        self.btn_broadway.clicked.connect(
            lambda: self.buttons_range(self.btn_broadway.text())
        )
        self.btn_suited.clicked.connect(
            lambda: self.buttons_range(self.btn_suited.text())
        )
        self.btn_clear.clicked.connect(self.clear_label)

        self.tEdit_range.textChanged.connect(self.tEditTextChangeEvent)

        self.checkBox_hoverMode.stateChanged.connect(self.Hover_method)

    def table_item_actions(self):

        for button in self.frameTableCards.findChildren(QtWidgets.QAbstractButton):
            button.clicked.connect(lambda: self.table_cards())

        self.btn_clear_table.clicked.connect(self.clear_table)
        self.btn_random_table.clicked.connect(self.get_random_table)

    def hand_item_actions(self):

        for button in self.frameHandCards.findChildren(QtWidgets.QAbstractButton):
            button.clicked.connect(lambda: self.hand_cards())

        self.btn_clear_hand.clicked.connect(self.clear_hand)
        self.btn_random_hand.clicked.connect(self.get_random_hand)
 
    
    def buttons_click_actions(self):
        """
        Contains all connections between buttons and actions
        """
        self.actionLoad.triggered.connect(
            lambda: self.menu_elements_action(self.actionLoad.text())
        )
        self.actionSave.triggered.connect(
            lambda: self.menu_elements_action(self.actionSave.text())
        )
        self.actionClose.triggered.connect(
            lambda: self.menu_elements_action(self.actionClose.text())
        )
        self.actionGame.triggered.connect(
            lambda: self.menu_elements_action(self.actionGame.text())
        )

        

        
    def eventFilter(self, obj, event):
        """
        Contains custom events
        """
        if event.type() == QEvent.Type.HoverEnter:
            sender = obj
            if type(sender) == QtWidgets.QPushButton:
                sender.nextCheckState()
                self.rangeButtonClicked(sender)

        if (
            event.type() == QEvent.Type.MouseButtonDblClick
            and obj is self.lbl_cnt_combos
        ):
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

    def get_list_of_pushed_buttons(self):
        """
        Function create list of buttons which Check state is True

        return: list, Range
        """
        list_of_pushed_button = []

        for button in self.gridLayoutWidget.findChildren(QtWidgets.QAbstractButton):
            if button.isChecked():
                list_of_pushed_button.append(button.text())
        range_view_of_pushed_buttons = Range(" ".join(list_of_pushed_button))
        return sorted(list_of_pushed_button), range_view_of_pushed_buttons


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec())
