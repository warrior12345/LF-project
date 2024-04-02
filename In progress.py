import sys
import pandas as pd
import sqlite3
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import (QApplication, QTableWidget, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog)
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
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
        connection = sqlite3.connect('test.db')
        df.to_sql('Loadfile',connection, if_exists='replace',index=False)

        ###Loading docs from SQL File to Table Widget
        query = "SELECT * FROM Loadfile"
        c = connection.cursor()
        c.execute('SELECT COUNT(*) FROM pragma_table_info(\'Loadfile\');')

        ##fetch number of column
        num_columns = c.fetchone()[0]
        
        result = connection.execute(query)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(num_columns)
        ##self.tableWidget.setHorizontalHeaderLabels(num_columns)



        for row_number, row_data in enumerate(result):
           self.tableWidget.insertRow(row_number)
           for column_number, data in enumerate(row_data):

                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        ##for row in header:
           ## self.tableWidget.insertRow(self.tableWidget.rowCount())
           ## for column, value in enumerate(row):
             ##   self.tableWidget.setItem(self.tableWidget.rowCount() -1, column, QtWidgets.QTableWidgetItem(str(data)))



        c.close()
        connection.close()



    #Load data file
    ##def convert():
        ##df = pd.read_table(fname, sep= "¶", quotechar="þ",engine='python')

    #create a sql db
        ##connection = sqlite3.connect('test.db')

        #load data to sql
        # fail;replace;replace
        ##df.to_sql('Loadfile',connection, if_exists='replace')
        ##connection.close()

    ##convert()

if __name__ == "__main__":

    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
