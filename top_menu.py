from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QFileDialog

from PyQt6.QtCore import *
from PyQt6.QtGui import *

import pandas as pd

import sys
from poker import Range
from utils import *

from window_trainer import Trainer_window 




class TopMenu(QtWidgets.QMainWindow):
    def menu_elements_action(self, menu_btn):
        """
        Actions for every item in the menu
        """
        twidget = self.treeWidget_range

        if menu_btn == "Load":

            fname = QFileDialog.getOpenFileName(
                self, "Open Excel File", "", self.tr("Excel files (*.xlsx *.xls *.xml)")
            )[0]
            try:
                df = pd.read_excel(fname, header=None)
                try:
                    Range(df.iloc[0, 2])
                except ValueError:
                    df = pd.read_excel(fname)

                for i in range(len(df.columns)):
                    df.iloc[:, i] = df.iloc[:, i].astype("str")

                current_top_lvl_items = [
                    twidget.topLevelItem(i).text(0)
                    for i in range(twidget.topLevelItemCount())
                ]

                for group in df.iloc[:, 0].unique():
                    tmp_df = df[df.iloc[:, 0] == group]
                    if group not in current_top_lvl_items:
                        top_item = QtWidgets.QTreeWidgetItem([group])
                        tmp_dict = {}
                        for cat in tmp_df.iloc[:, 1].values:
                            child_item = QtWidgets.QTreeWidgetItem([cat])
                            top_item.addChild(child_item)
                            tmp_dict[cat] = Range(
                                tmp_df[tmp_df.iloc[:, 1] == cat].iloc[:, 2].values[0]
                            )

                        self.dict_range[group] = tmp_dict
                        twidget.addTopLevelItem(top_item)
                    else:
                        top_item = twidget.topLevelItem(
                            current_top_lvl_items.index(group)
                        )
                        current_child_lvl_items = [
                            top_item.child(i).text(0)
                            for i in range(top_item.childCount())
                        ]

                        tmp_dict = {k: v for k, v in self.dict_range[group].items()}

                        for cat in tmp_df.iloc[:, 1].values:
                            if cat not in current_child_lvl_items:
                                child_item = QtWidgets.QTreeWidgetItem([cat])
                                tmp_dict[cat] = Range(
                                    tmp_df[tmp_df.iloc[:, 1] == cat]
                                    .iloc[:, 2]
                                    .values[0]
                                )

                            else:
                                new_name = cat + "_" + str(len(current_child_lvl_items))
                                child_item = QtWidgets.QTreeWidgetItem([new_name])
                                tmp_dict[new_name] = Range(
                                    tmp_df[tmp_df.iloc[:, 1] == cat]
                                    .iloc[:, 2]
                                    .values[0]
                                )

                            top_item.addChild(child_item)

                        self.dict_range[group] = tmp_dict

                self.statusBar().showMessage("Range loaded")
            except FileNotFoundError:
                pass

        if menu_btn == "Save":

            try:
                if twidget.topLevelItemCount() == 0:
                    if self.tEdit_range.toPlainText() == "":
                        self.customMessageBox(
                            "Warning message", "Please, select range", "Warning"
                        )
                        return
                    else:
                        df = pd.DataFrame(
                            {
                                "group": ["0"],
                                "category_name": ["current_range"],
                                "range": [self.tEdit_range.toPlainText()],
                            }
                        )

                else:
                    df_form = []
                    for i in range(twidget.topLevelItemCount()):
                        top_item = twidget.topLevelItem(i)
                        top_item_name = top_item.text(0)
                        for j in range(top_item.childCount()):
                            child = top_item.child(j)
                            child_name = child.text(0)
                            df_form.append(
                                (
                                    top_item_name,
                                    child_name,
                                    ", ".join(
                                        self.dict_range[top_item_name][
                                            child_name
                                        ].rep_pieces
                                    ),
                                )
                            )

                    df = pd.DataFrame(
                        df_form, columns=["group", "category_name", "range"]
                    )

                fname = QFileDialog.getSaveFileName(
                    self,
                    "Save Excel File",
                    "",
                    self.tr("Excel files (*.xlsx *.xls *.xml)"),
                )[0]

                try:
                    df.to_excel(fname, index=False)
                    self.statusBar().showMessage("Range saved")
                except Exception:
                    pass

            except Exception:
                pass

        if menu_btn == "Close":
            sys.exit()
        
        if menu_btn == "Game":
            ui = Trainer_window(self)
            ui.show()
