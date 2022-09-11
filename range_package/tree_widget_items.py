from PyQt6 import QtWidgets

from PyQt6.QtCore import *
from PyQt6.QtGui import *

class TreeWidgetItems(QtWidgets.QMainWindow):
    def display_range_by_item(self):
        """
        Connection between QListWidget item and buttons. Display choosen range
        """
        widget = self.treeWidget_range

        try:
            item = widget.currentItem()
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

            parent = item.parent()

            if parent:
                range_list = [
                    str(i) for i in self.dict_range[parent.text(0)][item.text(0)].hands
                ]

                for button in self.gridLayout.findChildren(QtWidgets.QAbstractButton):
                    if button.text() in range_list:
                        button.setChecked(True)
                    else:
                        button.setChecked(False)

                range_str = ", ".join(
                    self.dict_range[parent.text(0)][item.text(0)].rep_pieces
                )
                self.tEdit_range.setPlainText(range_str)

        except AttributeError:
            print("1")
            pass

    def treeWidget_buttons(self, btn_name):
        """
        Contains all buttons actions with QTreeWidget
        """

        widget = self.treeWidget_range

        if btn_name == "Add Range":
            try:
                item = widget.currentItem()
                parent = item.parent()
                if not parent:
                    current_child_lvl_items = [
                        item.child(i).text(0) for i in range(item.childCount())
                    ]

                    category_name = self.tEdit_name.toPlainText()

                    if category_name == "":
                        name = str(item.childCount())
                    else:
                        name = category_name
                    if name not in current_child_lvl_items:
                        childWidget = QtWidgets.QTreeWidgetItem(item)
                        childWidget.setText(0, name)
                        item.addChild(childWidget)

                    _, cur_range = self.get_list_of_pushed_buttons()
                    self.dict_range[item.text(0)][name] = cur_range

            except Exception:
                self.customMessageBox(
                    "Warning message", "Please, select category", "Warning"
                )

        elif btn_name == "Add Category":
            current_top_lvl_items = [
                widget.topLevelItem(i).text(0)
                for i in range(widget.topLevelItemCount())
            ]

            category_name = self.tEdit_name.toPlainText()
            if category_name == "":
                name = str(widget.topLevelItemCount())
            else:
                name = category_name

            if name not in current_top_lvl_items:
                widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([name]))
                self.dict_range[name] = {}

        elif btn_name == "Rename":
            try:
                item = widget.currentItem()
                parent = item.parent()

                category_name = self.tEdit_name.toPlainText()

                if parent:
                    current_items = [
                        parent.child(i).text(0) for i in range(parent.childCount())
                    ]
                else:
                    current_items = [
                        widget.topLevelItem(i).text(0)
                        for i in range(widget.topLevelItemCount())
                    ]

                if category_name == "":
                    name = "_"
                else:
                    name = category_name

                if (name not in current_items) and (not parent):
                    self.dict_range[name] = self.dict_range.pop(item.text(0))
                    item.setText(0, name)

                elif (name not in current_items) and (parent):
                    self.dict_range[parent.text(0)][name] = self.dict_range[
                        parent.text(0)
                    ].pop(item.text(0))
                    item.setText(0, name)
            except Exception:
                pass

        elif btn_name == "Delete":
            try:
                item = widget.currentItem()
                parent = item.parent()

                if parent:
                    parent.takeChild(parent.indexOfChild(item))
                    self.dict_range[parent.text(0)].pop(item.text(0))
                else:
                    index = widget.indexOfTopLevelItem(item)
                    widget.takeTopLevelItem(index)
                    self.dict_range.pop(item.text(0))
            except Exception:
                pass

    # Попытки сделать treeWidgetItem is Editable с последующей постпроверкой ... Но что-то работает херово
    # def rename_value(self):
    #     item = self.treeWidget_range.currentItem()
    #     item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)

    # def checkName(self, item, column):

    #     item_text = item.data(0,0)
    #     siblings = self.getSiblings(item)

    #     if item_text in siblings:
    #         print('Duplicate item')
    #         item.setData(0,0, 'Plese enter a new value')

    #         self.treeWidget_range.editItem(item)

    # def getSiblings(self, item):
    #     siblings = [self.treeWidget_range.topLevelItem(i).data(0,0) for i in range(self.treeWidget_range.topLevelItemCount())]
    #     item_text = item.data(0,0)

    #     if item_text in siblings:
    #         siblings.remove(item_text)

    #     return siblings
