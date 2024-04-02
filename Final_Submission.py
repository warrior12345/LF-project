import sys
import pandas as pd
import sqlite3
from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog)
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("version0.01.ui", self)

        action = self.findChild(QAction,"newfileAction")
        action.triggered.connect(self.selectFile)
        self.selectFile = QLineEdit()

    def selectFile(self):
        ##dir_name = QFileDialog.getExistingDirectory(self, "Select your file")
        fname = QFileDialog.getOpenFileName(self, "Select you file")
        fname = fname[0].replace("/","\\")
        print(fname)     ###(Testing Block)
        df = pd.read_table(fname, sep= "¶", quotechar="þ",engine='python')
        connection = sqlite3.connect('test.db')
        df.to_sql('Loadfile',connection, if_exists='replace')


        connection.close()

app =QApplication([])
window = MainWindow()
window.show()
app.exec()
