import sys
import pandas as pd
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("version0.01.ui", self)



        action = self.findChild(QAction,"newfileAction")
        action.triggered.connect(self.selectFile)
        self.selectFile = QLineEdit()
###Main Function####
    def selectFile(self,split):
        ##dir_name = QFileDialog.getExistingDirectory(self, "Select your file")-------------(To get directory)
        fname = QFileDialog.getOpenFileName(self, str("Open File"),"/home",str("Text (*.dat)"))
        fname = fname[0].replace("/","\\")
        print(fname)     ###(Testing Block)


        ###Reading .dat File and making connection to SQL DB, create db file
        df = pd.read_table(fname, sep= "¶", quotechar="þ",engine='python')
        connection = sqlite3.connect(fname+".db")
        df.to_sql("Working_Table",connection, if_exists='replace',index=False)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(fname+".db")
        self.model = QSqlTableModel()

        self.CategoryTableView = QTableView()
        self.CategoryTableView.setModel(self.model)
        self.setCentralWidget(self.CategoryTableView)

        self.model.setTable("Working_Table")
        self.model.select()
        self.show()


        connection.close()


if __name__ == "__main__":

    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
