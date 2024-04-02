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

        action2 = self.findChild(QAction,"actionMass_Replace")
        action2.triggered.connect(self.replace)

        self.selectFile = QLineEdit()


###Main Function####
    def selectFile(self,split):
        ##dir_name = QFileDialog.getExistingDirectory(self, "Select your file")-------------(To get directory)
        global fname
        fname = QFileDialog.getOpenFileName(self, str("Open File"),"/home",str("Text (*.dat)"))
        fname = fname[0].replace("/","\\")
        print(fname)     ###(Testing Block)


        ###Reading .dat File and making connection to SQL DB, create db file
        Encoding = ["mbcs","utf-8"]


        df = pd.read_table(fname,sep= "¶", quotechar="þ",engine='python',encoding=Encoding[1])
        global connection
        connection = sqlite3.connect(fname+".db")
        df.to_sql("Working_Table",connection, if_exists='replace',index=False)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(fname+".db")
        self.model = QSqlTableModel()

        global cur
        cur = connection.cursor()

        self.CategoryTableView = QTableView()
        self.CategoryTableView.setModel(self.model)
        self.setCentralWidget(self.CategoryTableView)

        self.model.setTable("Working_Table")
        self.model.select()
        self.show()
        global replace
        replace = cur.execute('ALTER TABLE Working_Table ADD New_col TEXT')

        connection.commit()





if __name__ == "__main__":

    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
