import sys
import pandas as pd
import sqlite3
import chardet
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog, QInputDialog)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction, QIcon

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("version0.01.ui", self)


        action = self.findChild(QAction,"newfileAction")
        action.triggered.connect(self.LF_import)



        action2 = self.findChild(QAction,"actionAdd_Field")
        action2.triggered.connect(self.add_col)

        action3 = self.findChild(QAction,"actionReplace")
        action3.triggered.connect(self.replace)


###Main Function####
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

####Adding a new column------------Need to work ,Not working with user input currently)
    def add_col(self):

        fieldname = QInputDialog()
        fieldname.setLabelText("Enter Field Name:")
        fieldname.setLabelText("Enter Field Name:2")
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


    def replace(self):
        conn = sqlite3.connect(fname+".db")
        cursor = conn.cursor()
        #ctu = column to update
        ctu1 = "Name"

        #cursor.execute("UPDATE Working_Table SET COLUMN {} = 'Roshni' WHERE Units = 'Dollars (millions)'")
        cursor.execute("UPDATE Working_Table SET Units = 'Roshni' WHERE Units = 'Dollars (millions)'")

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










if __name__ == "__main__":

    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
