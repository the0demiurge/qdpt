from PyQt5.QtWidgets import QMainWindow, QMessageBox

from pyqdpt import utils
from pyqdpt.models.profile_model import ProfileTableModel
from pyqdpt.register import RegisterDialog
from pyqdpt.utils.errors import ErrorBox
from pyqdpt.views.ui_profile import Ui_ProfileWindow


class ProfileWindow(QMainWindow):
    def __init__(self, keys=None):
        super(ProfileWindow, self).__init__()
        self.ui = Ui_ProfileWindow()
        self.ui.setupUi(self)
        self.dataModel = ProfileTableModel(self.ui.devicesView, keys=keys)
        self.ui.devicesView.setModel(self.dataModel)
        self.ui.devicesView.doubleClicked.connect(self.switchAction)
        self.ui.addButton.clicked.connect(self.addAction)
        self.ui.deleteButton.clicked.connect(self.delAction)
        self.ui.switchButton.clicked.connect(self.switchAction)

        self.registerDialog = RegisterDialog()
        self.refreshView()

    def switchAction(self):
        pass

    def delAction(self):
        row = self.ui.devicesView.currentIndex().row()
        info = self.dataModel.getKey(row, by='index')
        answer = QMessageBox.warning(self, "Confirmation", "Delete Device <b>{}: {}</b>?".format(info['owner'], info['serial']), QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.dataModel.deleteItem(row, by='index')
        self.refreshView()

    def addAction(self):
        self.registerDialog.exec()
        if self.registerDialog.value is not None:
            self.dataModel.appendItem(
                self.registerDialog.value['cert'],
                self.registerDialog.value['key'],
                self.registerDialog.value['device_id'],
                self.registerDialog.value['serial'],
                self.registerDialog.value['owner'],
            )
        self.refreshView()

    def refreshView(self):
        self.ui.deleteButton.setDisabled(self.dataModel.rowCount() == 0)
        self.ui.switchButton.setDisabled(self.dataModel.rowCount() == 0)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    profilewindow = ProfileWindow(keys=utils.keys.load_keys())
    profilewindow.show()
    app.exec_()
