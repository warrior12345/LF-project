from PyQt6.QtWidgets import QMainWindow, QApplication, QTableView
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel


class TableTest(QMainWindow):
    def __init__(self, parent = None):
        super(TableTest, self).__init__(parent)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName("test.db")
        self.model = QSqlTableModel()

        self.CategoryTableView = QTableView()
        self.CategoryTableView.setModel(self.model)
        self.setCentralWidget(self.CategoryTableView)

        self.model.setTable('Loadfile')
        self.model.select()
        self.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = TableTest()
    sys.exit(app.exec())
