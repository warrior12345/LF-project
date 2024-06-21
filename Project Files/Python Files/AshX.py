import sys
import pandas as pd
import sqlite3
import chardet
from PyQt6 import uic
from PyQt6.QtWidgets import (QMainWindow, QApplication, QTableView, QMainWindow, QToolBar, QLabel, QStatusBar, QLineEdit, QFileDialog, QInputDialog, QDialog)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtGui import QAction, QIcon
import csv

class MainWindow(QMainWindow, QDialog):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("UI Files\\version0.01.ui", self)


        action = self.findChild(QAction,"newfileAction")
        action.triggered.connect(self.LF_import)

        action2 = self.findChild(QAction,"actionAdd_Field")
        action2.triggered.connect(self.add_col)

        action3 = self.findChild(QAction,"actionMass_Replace")
        action3.triggered.connect(self.update_clm)

        action4 = self.findChild(QAction,"actionReplace")
        action4.triggered.connect(self.update_val)






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


####Adding a new column------------Need to work ,Not working with user input currently)
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

####Mass Replace Function###

    def update_clm(self):

        fieldname2 = QInputDialog()
        fieldname2.setLabelText("Column to Update")
        fieldname2.exec()

        clm_name =  fieldname2.textValue()

        fieldname3 = QInputDialog()
        fieldname3.setLabelText("Add updated value")
        fieldname3.exec()
                                                          ####Update function with intial parameter for target column name
        new_value = fieldname3.textValue()                ####Input for updated value




        conn = sqlite3.connect(fname+".db")
        cursor = conn.cursor() 

        conn.execute("UPDATE Working_Table SET " + clm_name + "=(?)",(new_value,))           ####Query for mass replace, ###(new_value,))---IN THIS EXTRA COMMA AT THE END IS UNPACKING OF TUPLE
        conn.commit()                                                                        ####execution



                                                     ####call to function
        # Refresh the model.
        self.model.setTable("Working_Table")
        self.model.select()
        self.show()
                ###Used to fetch all records, By default table view only fetch 256 records, which is problamatic and leads to data base lock###
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.model.rowCount()

####Selective Replace Function###
    def update_val(self):

        fieldname4 = QInputDialog()
        fieldname4.setLabelText("Target Column")
        fieldname4.exec()
        clm_name2 =  fieldname4.textValue()  



        fieldname5 = QInputDialog()
        fieldname5.setLabelText("Old value which needs to be replaced")
        fieldname5.exec()

        old_value = fieldname5.textValue()

        fieldname6 = QInputDialog()
        fieldname6.setLabelText("New Value")
        fieldname6.exec()

        new_value = fieldname6.textValue()


        conn = sqlite3.connect(fname+".db")
        cursor = conn.cursor()         

        conn.execute("UPDATE Working_Table SET " + clm_name2 + "=(?) WHERE " + clm_name2 + "=(?)",(new_value, old_value,))
        conn.commit()



        # Refresh the model.
        self.model.setTable("Working_Table")
        self.model.select()
        self.show()
                ###Used to fetch all records, By default table view only fetch 256 records, which is problamatic and leads to data base lock###
        while self.model.canFetchMore():
            self.model.fetchMore()
        self.model.rowCount()        




####Export Function
    def export(self):
        ui2 = uic.loadUi("Replace.ui", self)
        second_window = ui2.SecondWindow
        second_window.show()
        conn = sqlite3.connect(fname+".db")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Working_Table')
        results = cursor.fetchall()
        writer = csv.writer(open('export.dat', 'w', newline=''), delimiter='¶',quotechar='þ', quoting=csv.QUOTE_ALL)
        writer.writerow([column[0] for column in cursor.description])
        writer.writerows(results)





######Main Window closing#####
if __name__ == "__main__":

    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
