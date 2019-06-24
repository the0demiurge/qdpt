import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListView, QAbstractItemView, QInputDialog, QLineEdit, QMessageBox, QGridLayout
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import *

# ['QAbstractItemModel',
#  'QAbstractListModel',
#  'QAbstractProxyModel',
#  'QAbstractTableModel',
#  'QDirModel',
#  'QFileSystemModel',
#  'QIdentityProxyModel',
#  'QItemSelectionModel',
#  'QSortFilterProxyModel',
#  'QStandardItemModel',
#  'QStringListModel']


class listview(QWidget):
    def __init__(self):
        super(listview, self).__init__()
        self.mainlayout = QGridLayout()
        self.lv = QListView(self)
        self.mainlayout.addWidget(self.lv, 0, 0)
        self.list_data = list('aoeuaoeu')
        self.mdl = QStringListModel(self.list_data)
        self.lv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lv.setModel(self.mdl)
        self.lv.doubleClicked.connect(self.insertData)
        self.lv.clicked.connect(self.askQuestion)
        self.setLayout(self.mainlayout)

    def modifyData(self, data):
        curidx = self.lv.currentIndex()
        text = data.data()
        self.mdl.setData(curidx, text + '1')

    def insertData(self, data):
        string, isOK = QInputDialog.getText(self, 'Code', 'Authencation Code:')
        if isOK:
            curidx = self.lv.currentIndex()
            self.mdl.insertRows(curidx.row(), 1)
            self.mdl.setData(curidx, string)

    def showData(self):
        data = '\n'.join(self.mdl.stringList())
        QMessageBox.information(self, "data", data)

    def askQuestion(self):
        data = QMessageBox.warning(self, "Header", "Quit?", QMessageBox.No | QMessageBox.Help | QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
        msgbox = QMessageBox()
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.setText('ERROR')
        msgbox.setWindowTitle('Error!')
        msgbox.setDetailedText('aoeuaoue\nthis is details info\nhahaha\naaaaa')
        ret = msgbox.exec()
        print(ret)
        print(data == QMessageBox.Yes)
        if data == QMessageBox.Yes:
            QApplication.quit()


# ['QColorDialog',
#  'QDialog',
#  'QFileDialog',
#  'QFontDialog',
#  'QInputDialog',
#  'QProgressDialog']


app = QApplication(sys.argv)
lv = listview()
lv.show()
app.exec_()
