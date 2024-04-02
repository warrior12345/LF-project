import sys
import pandas as pd
import sqlite3
import chardet
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog, QInputDialog, QDialog)
from PyQt6.QtGui import QAction, QIcon
import csv

from PyQt6 import QtCore, QtGui, QtWidgets
from replace import Ui_Replace

class Ui_MainWindow(object):


    def LF_import(self,split):
        ##dir_name = QFileDialog.getExistingDirectory(self, "Select your file")-------------(To get directory)
        global fname
        fname = QFileDialog.getOpenFileName(self, str("Open File"),"/home",str("Text (*.dat)"))
        fname = fname[0].replace("/","\\")
        print("File Path is : "+fname)     ###(Testing Block)


        ####Encoding detection####

        with open(fname,"rb") as enc1:
            enc1 = enc1.read(200)

        detection = chardet.detect(enc1)
        enc2 = detection['encoding']
        print("Encoding is "+enc2,",Supported encodings are 'utf-8','ANSI = ISO-8859-9','Unicode'")


        match enc2:
            case"utf-8":
                Encoding = ("utf-8")

            case"UTF-16":
                Encoding = ("UTF-16")

            case"ISO-8859-9":
                Encoding = ("mbcs")


        ###Defyning encoding manually-----------------(Not used in current code)
        #Encoding = ["mbcs","UTF-16"]

        ###Reading .dat File and making connection to SQL DB, create db file
        df = pd.read_table(fname,sep= "¶", quotechar="þ",engine='python',encoding=Encoding)
        connection = sqlite3.connect(fname+".db")
        df.to_sql("Working_Table",connection, if_exists='replace',index=False)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(fname+".db")

        #cursor = connection.cursor()
        #column_names = [description[0] for description in cursor.description]
        #print(column_names)


        self.model = QSqlTableModel()

        self.CategoryTableView = QTableView()
        self.CategoryTableView.setModel(self.model)
        self.setCentralWidget(self.CategoryTableView)

        self.model.setTable("Working_Table")
        self.model.select()
        self.show()

        ###Used to fetch all records, By default table view only fetch 256 records, which is problamatic and leads to data base lock###
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.model.rowCount()



    def window1(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Replace()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(895, 582)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableView = QtWidgets.QTableView(parent=self.centralwidget)
        self.tableView.setObjectName("tableView")
        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 895, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFamily_Tools = QtWidgets.QMenu(parent=self.menubar)
        self.menuFamily_Tools.setObjectName("menuFamily_Tools")
        self.menuPath_Tools = QtWidgets.QMenu(parent=self.menubar)
        self.menuPath_Tools.setObjectName("menuPath_Tools")
        self.menuField_Update = QtWidgets.QMenu(parent=self.menubar)
        self.menuField_Update.setObjectName("menuField_Update")
        self.menuQC = QtWidgets.QMenu(parent=self.menubar)
        self.menuQC.setObjectName("menuQC")
        self.menuDate_And_Time = QtWidgets.QMenu(parent=self.menubar)
        self.menuDate_And_Time.setObjectName("menuDate_And_Time")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.newfileAction = QtGui.QAction(parent=MainWindow)
        self.newfileAction.setObjectName("newfileAction")
        self.actionInsert = QtGui.QAction(parent=MainWindow)
        self.actionInsert.setObjectName("actionInsert")
        self.actionSave = QtGui.QAction(parent=MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionTools = QtGui.QAction(parent=MainWindow)
        self.actionTools.setObjectName("actionTools")
        self.actionReplace = QtGui.QAction(parent=MainWindow)
        self.actionReplace.setObjectName("actionReplace")
        self.actionMass_Replace = QtGui.QAction(parent=MainWindow)
        self.actionMass_Replace.setObjectName("actionMass_Replace")
        self.actionAdd_Field = QtGui.QAction(parent=MainWindow)
        self.actionAdd_Field.setObjectName("actionAdd_Field")
        self.actionBuild_Family = QtGui.QAction(parent=MainWindow)
        self.actionBuild_Family.setObjectName("actionBuild_Family")
        self.actionPath_Update = QtGui.QAction(parent=MainWindow)
        self.actionPath_Update.setObjectName("actionPath_Update")
        self.actionRename_Files = QtGui.QAction(parent=MainWindow)
        self.actionRename_Files.setObjectName("actionRename_Files")
        self.actionRemove_Field = QtGui.QAction(parent=MainWindow)
        self.actionRemove_Field.setObjectName("actionRemove_Field")
        self.actionCompare_Loadfile = QtGui.QAction(parent=MainWindow)
        self.actionCompare_Loadfile.setObjectName("actionCompare_Loadfile")
        self.actionFormat_Date_and_Time = QtGui.QAction(parent=MainWindow)
        self.actionFormat_Date_and_Time.setObjectName("actionFormat_Date_and_Time")
        self.actionMerge_Date_And_Time = QtGui.QAction(parent=MainWindow)
        self.actionMerge_Date_And_Time.setObjectName("actionMerge_Date_And_Time")
        self.actionMerge_Fields = QtGui.QAction(parent=MainWindow)
        self.actionMerge_Fields.setObjectName("actionMerge_Fields")
        self.actionEncoding_Conversion = QtGui.QAction(parent=MainWindow)
        self.actionEncoding_Conversion.setObjectName("actionEncoding_Conversion")
        self.menuFile.addAction(self.newfileAction)
        self.menuFile.triggered.connect(self.LF_import)
        self.menuFile.addAction(self.actionInsert)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionTools)
        self.menuFile.addAction(self.actionEncoding_Conversion)
        self.menuFamily_Tools.addAction(self.actionBuild_Family)
        self.menuPath_Tools.addAction(self.actionPath_Update)
        self.menuPath_Tools.addAction(self.actionRename_Files)
        self.menuField_Update.addSeparator()
        self.menuField_Update.addAction(self.actionReplace)
        self.menuField_Update.triggered.connect(self.window1)
        self.menuField_Update.addAction(self.actionMass_Replace)
        self.menuField_Update.addAction(self.actionAdd_Field)
        self.menuField_Update.addAction(self.actionRemove_Field)
        self.menuField_Update.addAction(self.actionMerge_Fields)
        self.menuQC.addAction(self.actionCompare_Loadfile)
        self.menuDate_And_Time.addAction(self.actionFormat_Date_and_Time)
        self.menuDate_And_Time.addAction(self.actionMerge_Date_And_Time)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuField_Update.menuAction())
        self.menubar.addAction(self.menuFamily_Tools.menuAction())
        self.menubar.addAction(self.menuDate_And_Time.menuAction())
        self.menubar.addAction(self.menuPath_Tools.menuAction())
        self.menubar.addAction(self.menuQC.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AshX"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuFamily_Tools.setTitle(_translate("MainWindow", "Family Tools"))
        self.menuPath_Tools.setTitle(_translate("MainWindow", "Path Tools"))
        self.menuField_Update.setTitle(_translate("MainWindow", "Field Update"))
        self.menuQC.setTitle(_translate("MainWindow", "QC"))
        self.menuDate_And_Time.setTitle(_translate("MainWindow", "Date And Time"))
        self.newfileAction.setText(_translate("MainWindow", "New File"))
        self.actionInsert.setText(_translate("MainWindow", "Import"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionTools.setText(_translate("MainWindow", "Tools"))
        self.actionReplace.setText(_translate("MainWindow", "Replace"))
        self.actionMass_Replace.setText(_translate("MainWindow", "Mass Replace"))
        self.actionAdd_Field.setText(_translate("MainWindow", "Add Field"))
        self.actionBuild_Family.setText(_translate("MainWindow", "Build Family"))
        self.actionPath_Update.setText(_translate("MainWindow", "Path Update"))
        self.actionRename_Files.setText(_translate("MainWindow", "Rename Files"))
        self.actionRemove_Field.setText(_translate("MainWindow", "Remove Field"))
        self.actionCompare_Loadfile.setText(_translate("MainWindow", "Compare Loadfile"))
        self.actionFormat_Date_and_Time.setText(_translate("MainWindow", "Format  Date and Time"))
        self.actionMerge_Date_And_Time.setText(_translate("MainWindow", "Merge Date And Time"))
        self.actionMerge_Fields.setText(_translate("MainWindow", "Merge Fields"))
        self.actionEncoding_Conversion.setText(_translate("MainWindow", "Encoding Conversion"))







if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
