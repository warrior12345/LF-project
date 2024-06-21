import sys
import pandas as pd
import sqlite3
import chardet
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog, QInputDialog, QDialog)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction, QIcon
import csv

    def add_col(self):

        fieldname = QInputDialog()
        fieldname.setLabelText("Enter Field Name:")
        fieldname.exec()

        New_Col = fieldname.textValue()

        conn = sqlite3.connect(fname+".db")
        cursor = conn.cursor()

        cursor.execute("ALTER TABLE Working_Table ADD COLUMN {} TEXT".format(New_Col))

        conn.commit()
        conn.close()

        # Refresh the model.
        self.model.setTable("Working_Table")
        self.model.select()
        self.show()
                ###Used to fetch all records, By default table view only fetch 256 records, which is problamatic and leads to data base lock###
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.model.rowCount()