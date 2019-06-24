from pyqdpt import utils
from pyqdpt.models.profile_model import ProfileModel
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QApplication, QWidget, QListView, QAbstractItemView, QInputDialog, QLineEdit, QMessageBox, QGridLayout, QPushButton
import sys


k = utils.keys.load_keys()
pm = ProfileModel(k)

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
        self.insbtn = QPushButton('insert')
        self.delbtn = QPushButton('delete')
        self.mainlayout.addWidget(self.insbtn, 1, 0)
        self.mainlayout.addWidget(self.delbtn, 1, 1)
        self.mainlayout.addWidget(self.lv, 0, 0)
        self.list_data = list('aoeuaoeu')
        self.mdl = pm
        self.lv.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.lv.setModel(self.mdl)
        self.lv.doubleClicked.connect(self.insertData)
        # self.lv.clicked.connect(self.appendKey)
        # self.lv.clicked.connect(self.deleteKey)
        self.insbtn.clicked.connect(self.appendKey)
        self.delbtn.clicked.connect(self.deleteKey)
        self.delbtn.setDisabled(len(self.mdl) == 0)
        self.setLayout(self.mainlayout)

    def appendKey(self, ):
        string, isOK = QInputDialog.getText(self, 'Code', ' '.join(['cert', 'key', 'device_id', 'serial', 'owner']))
        if isOK:
            self.mdl.appendData(*string.split())
        else:
            self.mdl.appendData('cert', 'key', 'device_id', 'serial', 'owner')
        self.delbtn.setDisabled(len(self.mdl) == 0)

    def deleteKey(self):
        row = self.lv.currentIndex().row()
        info = self.mdl.getDescription(self.mdl.getKey(row, by='index'))
        answer = QMessageBox.warning(self, "Confirmation", "Delete Key <b>{}</b>?".format(info), QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        # answer = QMessageBox.question(self, "Confirmation", "Delete Key <b>{}</b>?".format(info))
        if answer == QMessageBox.Yes:
            self.mdl.deleteData(row, by='index')
        self.delbtn.setDisabled(len(self.mdl) == 0)

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
